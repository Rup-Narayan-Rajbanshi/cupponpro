import numpy as np
import pandas as pd
from django.db import transaction
from rest_framework import serializers

from commonapp.models.product import Product, ProductCategory
from data_manager.exception import DuplicateNameException, ProductCategoryNotExistException, \
    ProductCodeAlreadyExistException
from data_manager.helpers import create_or_update_from_dataframe
from helpers.serializer_fields import CharToNumericField
from helpers.validators import xlsx_validator, is_numeric_value
from helpers.misc import title_to_snake_case
from helpers.serializer import CustomBaseSerializer, CustomModelSerializer

ALLOWED_PRODUCT_TABLE_FIELDS = [
    'product_code', 'name', 'link', 'product_category', 'brand_name', 'purchase_price',
    'purchase_currency', 'selling_price', 'selling_currency']


class ProductSerializer(CustomModelSerializer):
    purchase_price = CharToNumericField(validators=[is_numeric_value], allow_null=True, allow_blank=True)

    class Meta:
        fields = ['product_code', 'name', 'link', 'brand_name',
                  'purchase_price', 'purchase_currency', 'selling_price', 'selling_currency']
        model = Product

    def validate(self, attrs):
        return super().validate(attrs)


class UploadExcelProductSerializer(CustomBaseSerializer):
    upload_file = serializers.FileField(required=True, validators=[xlsx_validator])

    class Meta:
        validators = []

    def validate(self, data, *args, **kwargs):
        company = self.context['request'].company

        df = pd.read_excel(data['upload_file'])
        df = df.replace(np.nan, '', regex=True)
        df.rename(columns={column_name: title_to_snake_case(column_name) for column_name in df.columns }, inplace=True)
        df['total_price'] = df['selling_price']

        # Validate product category name
        code_qs = Product.objects.filter(product_code__in=set(df['product_code']), company=company)

        if code_qs.exists():
            raise ProductCodeAlreadyExistException(list(code_qs.values_list('product_code', flat=True)))

        # Validate Product Data
        product_data = df.to_dict('records')
        serializer = ProductSerializer(data=product_data, many=True)
        serializer.is_valid(raise_exception=True)

        # Validate product category name
        product_categories_set = set(df['product_category'])

        category_qs = ProductCategory.objects.filter(name__in=product_categories_set)
        existing_product_categories = set(category_qs.values_list('name', flat=True))

        if len(product_categories_set - existing_product_categories) != 0:
            raise ProductCategoryNotExistException(product_categories_set - existing_product_categories)

        # Replace nan with blank
        # Prepare company for save
        df['company'] = str(company.id)
        df.rename(columns={'company': 'company_id'}, inplace=True)

        # Prepare product category for save
        category_name_id_map = {pc.name: pc.id for pc in category_qs}
        df['product_category'] = df['product_category'].apply(lambda x: str(category_name_id_map[x]))
        df.rename(columns={'product_category': 'product_category_id'}, inplace=True)

        df.rename(columns=lambda x: x.strip(), inplace=True)
        duplicates = df[df['name'].duplicated() == True]

        df['purchase_price'] = df['purchase_price'].apply(lambda x: int(x) if x else 0)

        # Name duplication validation
        duplicate_list = duplicates[duplicates['name'].duplicated() == False]['name'].tolist()
        if duplicate_list:
            raise DuplicateNameException(duplicate_list)
        # df['id_expiry_date'] = pd.to_datetime(df["id_expiry_date"]).dt.strftime('%Y-%m-%d')
        return df

    @transaction.atomic
    def save(self, validated_data, *args, **kwargs):
        create_or_update_from_dataframe(Product, validated_data, '', 'create')
        return True
