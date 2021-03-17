from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from inventory.models.expense import Expense, Payment
from rest_framework.exceptions import ValidationError
from helpers.constants import DEFAULTS
from helpers.choices_variable import PAYMENT_CHOICES


class ExpenseSerializer(CustomModelSerializer):
    expense_for = serializers.CharField(max_length=128)

    class Meta:
        model = Expense
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            company = getattr(request, 'company', None)
            if company:
                attrs['company'] = company
        return attrs




class PaymentSerializer(CustomModelSerializer):
    payment_note = serializers.CharField(max_length=128)
    payment_mode = serializers.ChoiceField(PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])

    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            company = getattr(request, 'company', None)
            if company:
                attrs['company'] = company
        return attrs