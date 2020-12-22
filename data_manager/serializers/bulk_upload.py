import pandas as pd
import numpy as np
from django.db import transaction
from rest_framework import serializers

from commonapp.models.product import Product
from data_manager.exception import DuplicateNameException
from data_manager.helpers import create_or_update_from_dataframe
from helpers.serializer import CustomBaseSerializer

ALLOWED_PRODUCT_TABLE_FIELDS = [
    'product_code', 'name', 'link', 'product_category', 'brand_name', 'purchase_price',
    'purchase_currency', 'selling_price', 'selling_currency']


class UploadExcelProductSerializer(CustomBaseSerializer):
    upload_file = serializers.FileField(required=True)

    class Meta:
        validators = []

    def validate(self, data, *args, **kwargs):
        df = pd.read_excel(data['upload_file'])
        df = df.replace(np.nan, '', regex=True)
        # Field name in db is different than in sheet. So df has to be renamed
        df.rename(columns={'account_name': 'full_name'}, inplace=True)
        df.rename(columns=lambda x: x.strip(), inplace=True)
        duplicates = df[df['name'].duplicated() == True]
        duplicate_list = duplicates[duplicates['name'].duplicated() == False]['name'].tolist()
        if duplicate_list:
            raise DuplicateNameException(duplicate_list)
        df['customer_code'] = df['customer_code'].astype(str).str.strip()
        df['id_expiry_date'] = pd.to_datetime(df["id_expiry_date"]).dt.strftime('%Y-%m-%d')
        df['date_of_birth'] = pd.to_datetime(df["date_of_birth"]).dt.strftime('%Y-%m-%d')
        df['valid_till'] = pd.to_datetime(df["valid_till"]).dt.strftime('%Y-%m-%d')
        df_ = df[ALLOWED_PRODUCT_TABLE_FIELDS + ['credit_limit', ]]
        return df

    @transaction.atomic
    def save(self, validated_data, *args, **kwargs):
        df = validated_data
        df_product = df[df.columns.intersection(ALLOWED_PRODUCT_TABLE_FIELDS)]

        # Create customer first to get customer_idx
        create_or_update_from_dataframe(Product, df_product, '', 'create')
        return True
