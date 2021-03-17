import numpy as np
import pandas as pd
from django.db import transaction
from rest_framework import serializers

from inventory.models.supplier import Supplier
from inventory.models.stock import Stock
from rest_framework.exceptions import ValidationError
from data_manager.exception import DuplicateNameException
from data_manager.helpers import create_or_update_from_dataframe
from helpers.serializer_fields import CharToNumericField
from helpers.validators import xlsx_validator, is_numeric_value
from helpers.misc import title_to_snake_case
from helpers.serializer import CustomBaseSerializer, CustomModelSerializer
from helpers.constants import PRODUCT_TYPE
ALLOWED_PRODUCT_TABLE_FIELDS = [
    'product_code', 'name', 'link', 'product_category', 'brand_name', 'purchase_price',
    'purchase_currency', 'selling_price', 'selling_currency']


class SupplierSerializer(CustomModelSerializer):
    purchase_price = CharToNumericField(validators=[is_numeric_value], allow_null=True, allow_blank=True)

    class Meta:
        fields = '__all__'
        model = Supplier

    def validate(self, attrs):
        return super().validate(attrs)


class UploadExcelSupplierSerializer(CustomBaseSerializer):
    upload_file = serializers.FileField(required=True, validators=[xlsx_validator])

    class Meta:
        validators = []

    def validate(self, data, *args, **kwargs):
        company = self.context['request'].company

        df = pd.read_excel(data['upload_file'])
        df = df.replace(np.nan, '', regex=True)
        df.rename(columns={column_name: title_to_snake_case(column_name) for column_name in df.columns }, inplace=True)
        valid_column = ['name', 'company']

        valid_column=list(set(valid_column))
        columns = list(set(df.columns))
        if not all(item in valid_column for item in columns):
            raise ValidationError({'detail': 'Invalid file format.'})


        # name check
        code_qs = Supplier.objects.filter(name__in=set(df['name']), company=company)

        if code_qs.exists():
            raise ValidationError({'supplier already exists'})


        # Prepare company for save
        df['company'] = str(company.id)
        df.rename(columns={'company': 'company_id'}, inplace=True)

        # Validate Product Data
        product_data = df.to_dict('records')
        serializer = SupplierSerializer(data=product_data, many=True)
        serializer.is_valid(raise_exception=True)


        df.rename(columns=lambda x: x.strip(), inplace=True)
        duplicates = df[df['name'].duplicated() == True]


        # Name duplication validation
        duplicate_list = duplicates[duplicates['name'].duplicated() == False]['name'].tolist()
        if duplicate_list:
            raise DuplicateNameException(duplicate_list)
        return df

    @transaction.atomic
    def save(self, validated_data, *args, **kwargs):
        create_or_update_from_dataframe(Supplier, validated_data, '', 'create')
        return True








class StockSerializer(CustomModelSerializer):

    class Meta:
        fields = '__all__'
        model = Stock

    def validate(self, attrs):
        return super().validate(attrs)


class UploadExcelStockSerializer(CustomBaseSerializer):
    upload_file = serializers.FileField(required=True, validators=[xlsx_validator])

    class Meta:
        validators = []

    def validate(self, data, *args, **kwargs):
        company = self.context['request'].company

        df = pd.read_excel(data['upload_file'])
        df = df.replace(np.nan, '', regex=True)
        df.rename(columns={column_name: title_to_snake_case(column_name) for column_name in df.columns }, inplace=True)
        valid_column = ['name', 'company', 'stock', 'minimum_quantity', 'unit']

        valid_column=list(set(valid_column))
        columns = list(set(df.columns))
        if not all(item in valid_column for item in columns):
            raise ValidationError({'detail': 'Invalid file format.'})


        # name check
        code_qs = Stock.objects.filter(name__in=set(df['name']), company=company)

        if code_qs.exists():
            raise ValidationError({'stock already exists'})


        # Prepare company for save
        df['company'] = str(company.id)
        df.rename(columns={'company': 'company_id'}, inplace=True)

        # Validate Product Data
        product_data = df.to_dict('records')
        serializer = StockSerializer(data=product_data, many=True)
        serializer.is_valid(raise_exception=True)


        df.rename(columns=lambda x: x.strip(), inplace=True)
        duplicates = df[df['name'].duplicated() == True]


        # Name duplication validation
        duplicate_list = duplicates[duplicates['name'].duplicated() == False]['name'].tolist()
        if duplicate_list:
            raise DuplicateNameException(duplicate_list)
        return df

    @transaction.atomic
    def save(self, validated_data, *args, **kwargs):
        create_or_update_from_dataframe(Stock, validated_data, '', 'create')
        return True