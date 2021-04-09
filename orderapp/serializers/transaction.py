from helpers.serializer import CustomModelSerializer
from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from orderapp.models.transaction import TransactionHistoryBills, Complimentary
from orderapp.models.bills import Bills
from orderapp.models.order import Orders
from orderapp.choice_variables import PAYMENT_CHOICES
from orderapp.constants import DEFAULTS
from userapp.models.user import User


class TransactionHistoryBillSerializer(CustomModelSerializer):
    bill = DetailRelatedField(model=Bills, lookup='id', representation = 'order_representation')
    paid_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required = True)
    return_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=True)
    credit_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=True)
    payment_mode = serializers.ChoiceField(PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'], required=False)
    customer = serializers.SerializerMethodField()
    asset = serializers.SerializerMethodField()

    class Meta:
        model = TransactionHistoryBills
        fields = '__all__'

    def get_customer(self, obj):
        try:
            customer = obj.bill.customer
        except:
            customer=None
        data = dict()
        if customer:
            data={'id':customer.id, 'name':customer.name}
        return data

    def get_asset(self, obj):
        try:
            asset = obj.bill.orders.first().asset
        except:
            asset = None
        data={}
        if asset:
            data={'id': asset.id, 'name':asset.name}
        return data



class ComplimentarySerializer(CustomModelSerializer):
    order = DetailRelatedField(model=Orders, lookup='id', representation='to_representation')
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation', required=False, allow_null=True)


    class Meta:
        model = Complimentary
        fields = '__all__'