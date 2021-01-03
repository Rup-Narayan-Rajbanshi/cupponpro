from django.db import transaction
from rest_framework import serializers

from helpers.constants import ORDER_STATUS
from helpers.serializer import CustomModelSerializer
from orderapp.models.bills import Bills
from orderapp.models.order import Orders
from orderapp.serializers.order import TableOrderCreateSerializer


class BillCreateSerializer(CustomModelSerializer):

    class Meta:
        model = Bills
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)


class ManualBillCreateSerializer(TableOrderCreateSerializer):

    # class Meta:
    #     model = Orders
    #     fields = ('id', 'voucher', 'asset', 'order_lines', 'bill')

    @transaction.atomic
    def create(self, validated_data):
        validated_data['status'] = ORDER_STATUS['BILLABLE']
        order = super().create(validated_data)
        first_line = order.lines.first()
        data = dict()
        data['is_manual'] = True
        data['company'] = order.company.id
        data['tax'] = order.company.tax if order.company.tax else 0
        data['service_charge'] = order.company.service_charge if order.company.service_charge else 0
        serializer = BillCreateSerializer(data=data, context={'request': self.context['request']})
        if not serializer.is_valid():
            raise serializers.ValidationError(detail='Cannot bill the order', code=400)
        order.bill = serializer.save()
        if first_line and first_line.voucher:
            order.user = first_line.voucher.user
        order.save()
        return order
