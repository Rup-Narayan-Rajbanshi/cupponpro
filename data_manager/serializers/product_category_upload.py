import numpy as np
import pandas as pd
from django.db import transaction
from rest_framework import serializers

from company.models.company import Company
from rest_framework.exceptions import ValidationError
from productapp.models.product import ProductCategory
from data_manager.exception import DuplicateNameException, ProductCategoryAlreadyExistException
from data_manager.helpers import create_or_update_from_dataframe
from helpers.misc import title_to_snake_case
from helpers.serializer_fields import DetailRelatedField
from helpers.validators import xlsx_validator
from helpers.serializer import CustomBaseSerializer, CustomModelSerializer
from helpers.constants import PRODUCT_CAT_TYPE

ALLOWED_PRODUCT_CATEGORY_FIELDS = ['name', 'link', 'company']


class ProductCategorySerializer(CustomModelSerializer):

    class Meta:
        fields = ['name', 'link']
        model = ProductCategory

    def validate(self, attrs):
        return super().validate(attrs)


class UploadExcelProductCategorySerializer(CustomBaseSerializer):
    upload_file = serializers.FileField(required=True, validators=[xlsx_validator])

    class Meta:
        validators = []

    def validate(self, data, *args, **kwargs):
        company = self.context['request'].company
        df = pd.read_excel(data['upload_file'])
        df.rename(columns={column_name: title_to_snake_case(column_name) for column_name in df.columns},
                  inplace=True)

        valid_column = ['parent', 'name', 'link', 'company', 'image',
       'token', 'types', 'sub_type', 'position']

        valid_column=list(set(valid_column))
        columns = list(set(df.columns))

        if not all(item in valid_column for item in columns):
            raise ValidationError({'detail': 'Invalid file format.'})

        if 'types' in columns:
            value = df['types'].unique()
            for val in value:
                if val not in list(PRODUCT_CAT_TYPE.keys()):
                    raise ValidationError({'detail': 'Types only take FOOD, BAR or COFFEE as value. '})

        # Replace nan with blank
        df = df.replace(np.nan, '', regex=True)

        # Validate product category name
        category_qs = ProductCategory.objects.filter(name__in=set(df['name']), company=company)

        if category_qs.exists():
            raise ProductCategoryAlreadyExistException(list(category_qs.values_list('name', flat=True)))

        # Prepare company for save
        df['company'] = str(company.id)

        # Validate Customer Data
        category_data = df.to_dict('records')
        serializer = ProductCategorySerializer(data=category_data, many=True)
        serializer.is_valid(raise_exception=True)

        df.rename(columns={'company': 'company_id'}, inplace=True)

        df.rename(columns=lambda x: x.strip(), inplace=True)
        duplicates = df[df['name'].duplicated() == True]

        # Name duplication validation
        duplicate_list = duplicates[duplicates['name'].duplicated() == False]['name'].tolist()
        if duplicate_list:
            raise DuplicateNameException(duplicate_list)
        # df['id_expiry_date'] = pd.to_datetime(df["id_expiry_date"]).dt.strftime('%Y-%m-%d')

        return df

    @transaction.atomic
    def save(self, validated_data, *args, **kwargs):
        create_or_update_from_dataframe(ProductCategory, validated_data, '', 'create')
        return True
