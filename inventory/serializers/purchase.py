from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from inventory.models.purchase import Purchase, PurchaseTransaction
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import DetailRelatedField
from helpers.constants import DEFAULTS
from helpers.choices_variable import PURCHASE_STATUS_CHOICES, PAYMENT_CHOICES, STOCK_TRANSACTION_CHOICES
from inventory.models.stock import Stock
from inventory.models.supplier import Supplier
from django.utils import timezone
from notifications.constants import NOTIFICATION_CATEGORY_NAME, NOTIFICATION_CATEGORY




class PurchaseSerializer(CustomModelSerializer):
    document = serializers.FileField(required=False)
    payment_mode = serializers.ChoiceField(PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])
    status = serializers.ChoiceField(PURCHASE_STATUS_CHOICES, default=DEFAULTS['PURCHASE_STATUS'])
    stock = DetailRelatedField(model=Stock, lookup='id', representation='to_representation', required=False, allow_null=True)
    supplier = DetailRelatedField(model=Supplier, lookup='id', representation='to_representation', required=False, allow_null=True)
    types = serializers.ChoiceField(STOCK_TRANSACTION_CHOICES, default=DEFAULTS['STOCK_TRANSACTION'])
    paid_date = serializers.DateField(required=False, allow_null=True)
    payment_note = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Purchase
        fields = "__all__"

    def validate(self, attrs):
        return attrs


    def create(self, validated_data):
        purchase, stock = Purchase.create_purchase(**validated_data)
        if stock.stock < stock.minimum_quantity:
            from notifications.tasks import notify_company_staffs
            company = str(stock.company.id)
            message = 'Stock is low. '
            payload = {
                'id': str(stock.id),
                'category': NOTIFICATION_CATEGORY_NAME['STOCK_LOW'],
                'message': {
                    'en': message
                }
            }
            try:
                notify_company_staffs(
                    company, NOTIFICATION_CATEGORY['STOCK_LOW'], payload)
                pass
            except:
                pass
        validated_data.pop('payment_note', '')
        validated_data.pop('paid_date', timezone.now)
        return purchase

    def update(self, instance, validated_data):
        purchase = Purchase.update_purchase(instance, **validated_data)
        payment_note = validated_data.pop('payment_note', '')
        paid_date = validated_data.pop('paid_date', timezone.now)
        return purchase







class PurchaseTransactionSerializer(CustomModelSerializer):
    purchase = DetailRelatedField(model=Purchase, lookup='id', representation='to_representation')

    class Meta:
        model = PurchaseTransaction
        fields = "__all__"
