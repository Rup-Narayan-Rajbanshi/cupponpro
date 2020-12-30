from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from commonapp.models.asset import Asset
from commonapp.models.coupon import Voucher
from commonapp.models.order import Order
from helpers.serializer import CustomModelSerializer
from helpers.constants import ORDER_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES
from helpers.serializer_fields import DetailRelatedField
from orderapp.models.order import OrderLines, Orders
from orderapp.serializers.order_line import OrderLineSerializer


class OrderStatusSerializer(CustomModelSerializer):
    status = serializers.ChoiceField(ORDER_STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ('status', )

    def validate(self, attrs):
        status = attrs['status']
        allowed_status_change = {
            ORDER_STATUS['NEW_ORDER']: [ORDER_STATUS['CONFIRMED'], ORDER_STATUS['CANCELLED']],
            ORDER_STATUS['CONFIRMED']: [ORDER_STATUS['PROCESSING']],
            ORDER_STATUS['PROCESSING']: [ORDER_STATUS['BILLABLE']],
            ORDER_STATUS['BILLABLE']: [],
            ORDER_STATUS['CANCELLED']: []
        }

        if self.instance is not None:
            instance = self.instance
            if status not in allowed_status_change[instance.status]:
                raise ValidationError({'detail': 'Cannot change status from {} to {}.'.format(instance.status, status)})
        return attrs

    def update(self, instance, validated_data):
        request = self.context.get('request')
        order = Orders.execute_change_status(order=instance, v_data=validated_data, request=request)
        return order


class TableStatusChangeSerializer(OrderStatusSerializer):

    class Meta:
        model = Orders
        fields = ('status', )

    def update(self, instance, validated_data):
        order = super(TableStatusChangeSerializer, self).update(instance, validated_data)
        order.lines.update()
        return order


class TableOrderCreateSerializer(CustomModelSerializer):
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation')
    voucher = DetailRelatedField(model=Voucher, lookup='id', representation='to_representation', required=False)
    order_lines = OrderLineSerializer(many=True, required=True)

    class Meta:
        model = Orders
        fields = ('id', 'voucher', 'asset', 'order_lines')

    def get_fields(self):
        fields = super().get_fields()
        if self.context['request'].method == 'GET':
            fields['order_lines'] = serializers.SerializerMethodField('lines')
        return fields

    def lines(self, order):
        lines = OrderLineSerializer(order.lines.all(), many=True)
        return lines.data

    def validate(self, attrs):
        if self.instance:
            if self.context['request'].company != self.instance.company:
                raise ValidationError('Cannot update for another company')
        elif attrs['asset'].orders.filter(status__in=[
            ORDER_STATUS['NEW_ORDER'],
            ORDER_STATUS['PROCESSING'],
            ORDER_STATUS['CONFIRMED']]).exists():

            raise ValidationError('Table already has an active order')
        return super().validate(attrs)

    def build_orderline_bulk_create_data(self, order, validated_order_line_data, voucher):
        bulk_create_data = list()
        for line in validated_order_line_data:
            order_line = OrderLines(order=order,
                                    product=line['product'],
                                    quantity=int(line['quantity']),
                                    rate=float(line['product'].total_price),
                                    voucher=voucher)
            order_line.discount = order_line.get_discount()
            order_line.discount_amount = order_line.get_discounted_amount()
            order_line.total = order_line.get_line_total()
            bulk_create_data.append(order_line)
        return bulk_create_data

    @transaction.atomic
    def create(self, validated_data):
        self.fields.pop('order_lines')
        self.fields.pop('voucher')
        order_lines = validated_data.pop('order_lines')
        voucher = validated_data.pop('voucher') if validated_data.get('voucher') else None

        validated_data['user'] = self.context['request'].user
        validated_data['company'] = self.context['request'].company
        order = super().create(validated_data)

        order_line_bulk_create_data = self.build_orderline_bulk_create_data(order, order_lines, voucher)
        OrderLines.objects.bulk_create(order_line_bulk_create_data)
        return order
