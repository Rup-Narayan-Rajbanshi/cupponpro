from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from commonapp.models.asset import Asset
from commonapp.models.coupon import Voucher
from commonapp.models.order import Order
from helpers.serializer import CustomModelSerializer, CustomBaseSerializer
from helpers.constants import ORDER_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES
from helpers.serializer_fields import DetailRelatedField
from helpers.validators import is_numeric_value
from notifications.constants import NOTIFICATION_CATEGORY_NAME, NOTIFICATION_CATEGORY
from orderapp.choice_variables import PAYMENT_CHOICES
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
        order = Order.execute_change_status(order=instance, v_data=validated_data, request=request)
        return order


class TableOrderSerializer(OrderStatusSerializer):
    payment_mode = serializers.ChoiceField(choices=PAYMENT_CHOICES, required=False)
    custom_discount_percentage = serializers.CharField(validators=[is_numeric_value], required=False)
    voucher = DetailRelatedField(model=Voucher, lookup='id',
                                 representation='to_representation', required=False)

    class Meta:
        model = Orders
        fields = ('status', 'payment_mode', 'custom_discount_percentage', 'voucher')

    def validate(self, attrs):
        # if not attrs.get('payment_mode') and attrs['status'] == ORDER_STATUS['COMPLETED']:
        #     raise ValidationError('Please enter payment mode')
        status = attrs['status']
        allowed_status_change = {
            # ORDER_STATUS['NEW_ORDER']: [ORDER_STATUS['CONFIRMED'], ORDER_STATUS['CANCELLED']],
            # ORDER_STATUS['CONFIRMED']: [ORDER_STATUS['PROCESSING']],
            # ORDER_STATUS['PROCESSING']: [ORDER_STATUS['BILLABLE']],
            # ORDER_STATUS['BILLABLE']: [],
            # ORDER_STATUS['CANCELLED']: [],
            # ORDER_STATUS['COMPLETED']: ['BILLABLE']
        }

        if self.instance.status in [ORDER_STATUS['CANCELLED'], ORDER_STATUS['COMPLETED']]:
            # instance = self.instance
            # if status not in allowed_status_change[instance.status]:
            raise ValidationError({'detail': 'Cannot change status from {} to {}.'.format(self.instance.status, status)})
        return attrs

    def update(self, instance, validated_data):
        request = self.context.get('request')
        voucher = validated_data.get('voucher')
        if voucher:
            for line in instance.lines.all():
                line.update(voucher=voucher)
        order = Orders.execute_change_status(order=instance, v_data=validated_data, request=request)
        return order


class CompanyTableOrderSerializer(CustomModelSerializer):
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation', required=True)
    voucher = DetailRelatedField(model=Voucher, lookup='id', representation='to_representation',
                                 required=False, allow_null=True)
    order_lines = OrderLineSerializer(many=True, required=True)
    price_details = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('id', 'status', 'voucher', 'asset', 'order_lines', 'price_details')

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        if request and request.method == 'GET':
            fields['order_lines'] = serializers.SerializerMethodField('lines')
        return fields

    def lines(self, order):
        lines = OrderLineSerializer(order.lines.all(), many=True)
        return lines.data

    def get_price_details(self, obj):
        return {
            'discount': obj.discount_amount,
            'sub_total': obj.subtotal,
            'tax': obj.company.tax,
            'service_charge': obj.company.service_charge,
            'grand_total': obj.grand_total
        }

    def validate(self, attrs):
        if self.instance:
            if self.context['request'].company != self.instance.company:
                raise ValidationError('Cannot update for another company')
            if self.instance.status in [ORDER_STATUS['CANCELLED'], ORDER_STATUS['COMPLETED']]:
                raise ValidationError('Cannot update completed or cancelled order')
        elif attrs['asset'].orders.filter(status__in=[
            ORDER_STATUS['NEW_ORDER'],
            ORDER_STATUS['PROCESSING'],
            ORDER_STATUS['BILLABLE'],
            ORDER_STATUS['CONFIRMED']]
            # user__companyuser__user__group__name__in=['sales', 'manager', 'owner', 'user']
        ).exists():
            raise ValidationError('Table already has an active order')
        return super().validate(attrs)

    def build_orderline_bulk_create_data(self, order, validated_order_line_data, voucher, served_products=None):
        bulk_create_data = list()
        for line in validated_order_line_data:
            new_quantity = int(line['quantity'])
            order_line = OrderLines(order=order,
                                    product=line['product'],
                                    status=line.get('status', 'NEW'),
                                    new=line.get('new', 0),
                                    cooking=line.get('cooking', 0),
                                    served=line.get('served', 0),
                                    quantity=new_quantity,
                                    rate=float(line['product'].total_price),
                                    voucher=voucher)
            # old_served_quantity = served_products.get(str(order_line.product_id))
            # if old_served_quantity:
            #     order_line.quantity = old_served_quantity if old_served_quantity > new_quantity else new_quantity - old_served_quantity
            order_line.discount = order_line.get_discount()
            order_line.discount_amount = order_line.get_discounted_amount()
            order_line.total = order_line.get_line_total()
            bulk_create_data.append(order_line)
        return bulk_create_data

    @transaction.atomic
    def create(self, validated_data, notify=True):
        from notifications.tasks import notify_company_staffs
        self.fields.pop('order_lines')
        self.fields.pop('voucher')
        order_lines = validated_data.pop('order_lines')
        voucher = validated_data.pop('voucher', None)
        validated_data['user'] = self.context['request'].user
        if not validated_data['user'].is_authenticated:
            validated_data['user'] = None
        if voucher:
            validated_data['user'] = voucher.user
        validated_data['company'] = self.context['request'].company

        order = super().create(validated_data)

        order_line_bulk_create_data = self.build_orderline_bulk_create_data(order, order_lines, voucher)
        OrderLines.objects.bulk_create(order_line_bulk_create_data)
        # if order.lines.exclude(status__in='SERVED').count() == 0:
        #     order.update(status=ORDER_STATUS['BILLABLE'])
        if notify:
            company = str(order.company.id)
            if order.asset:
                message = 'New order is placed from {0} {1}'.format(order.asset.asset_type, order.asset.name)
            else:
                message = 'A new order is placed'
            payload = {
                'id': str(order.id),
                'category': NOTIFICATION_CATEGORY_NAME['ORDER_PLACED'],
                'message': {
                    'en': message
                }
            }
            try:
                notify_company_staffs.apply_async(kwargs={
                                    'company': company,
                                    'category': NOTIFICATION_CATEGORY['ORDER_PLACED'],
                                    'payload': payload,
                                    'asset': validated_data.get('asset')
                                })
                pass
            except:
                pass
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        from notifications.tasks import notify_company_staffs
        self.fields.pop('order_lines')
        self.fields.pop('voucher')
        order_lines = validated_data.pop('order_lines')
        voucher = validated_data.pop('voucher', None)
        validated_data['user'] = self.context['request'].user
        if not validated_data['user'].is_authenticated:
            validated_data['user'] = None
        if voucher:
            validated_data['user'] = voucher.user
        validated_data['company'] = self.context['request'].company
        served_products = dict()
        for line in instance.lines.all():
            # if line.status == 'SERVED':
            #     served_products[str(line.product.id)] = line.quantity
            # else:
            line.delete(force_delete=True)
        order_line_bulk_create_data = self.build_orderline_bulk_create_data(instance, order_lines, voucher,
                                                                            served_products)
        OrderLines.objects.bulk_create(order_line_bulk_create_data)
        order = super().update(instance, validated_data)
        company = str(order.company.id)
        payload = {
            'id': str(order.id),
            'category': NOTIFICATION_CATEGORY_NAME['ORDER_UPDATED'],
            'message': {
                'en': 'Order is Updated from {0} {1}'.format(order.asset.asset_type, order.asset.name)
            }
        }
        try:
            notify_company_staffs.apply_async(kwargs={
                'company': company,
                'category': NOTIFICATION_CATEGORY['ORDER_UPDATED'],
                'payload': payload,
                'asset': validated_data.get('asset')
            })
            pass
        except:
            pass
        return order


class UserOrderSerializerCompany(CompanyTableOrderSerializer):
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation',
                               required=False, allow_null=True)

    def validate(self, attrs):
        asset = attrs.get('asset', None)
        if asset and asset.orders.filter(status__in=[
            ORDER_STATUS['NEW_ORDER'],
            ORDER_STATUS['PROCESSING'],
            ORDER_STATUS['BILLABLE'],
            ORDER_STATUS['CONFIRMED']],
            # user__companyuser__user__group__name__in=['sales', 'manager', 'owner']
        ).exists():
            raise ValidationError('Table already has an active order')
        return attrs
