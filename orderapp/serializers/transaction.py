from helpers.serializer import CustomModelSerializer
from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from orderapp.models.transaction import TransactionHistoryBills

class TransactionHistoryBillSerializer(CustomModelSerializer):
    paid_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required = True)
    return_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=True)
    credit_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=True)

    class Meta:
        model = TransactionHistoryBills
        fields = '__all__'