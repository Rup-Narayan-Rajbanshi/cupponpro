from helpers.serializer import CustomModelSerializer
from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from orderapp.models.transaction import TransactionHistoryBills
from orderapp.models.bills import Bills
from orderapp.choice_variables import PAYMENT_CHOICES
from orderapp.constants import DEFAULTS

class TransactionHistoryBillSerializer(CustomModelSerializer):
    bill = DetailRelatedField(model=Bills, lookup='id', representation = 'order_representation')
    paid_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required = True)
    return_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=True)
    credit_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=True)
    payment_mode = serializers.ChoiceField(PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'], required=False)

    class Meta:
        model = TransactionHistoryBills
        fields = '__all__'