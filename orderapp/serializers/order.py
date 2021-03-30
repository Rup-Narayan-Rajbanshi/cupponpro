from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from company.models.company import Company
from company.models.partner import DeliveryPartner
from company.models.asset import Asset
from productapp.models.coupon import Voucher
from commonapp.models.order import Order
from helpers.serializer import CustomModelSerializer, CustomBaseSerializer
from helpers.constants import ORDER_STATUS, ORDER_LINE_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES, ASSET_TYPE_CHOICES
from helpers.serializer_fields import DetailRelatedField
from helpers.validators import is_numeric_value, is_percentage
from notifications.constants import NOTIFICATION_CATEGORY_NAME, NOTIFICATION_CATEGORY
from orderapp.choice_variables import PAYMENT_CHOICES
from orderapp.models.order import OrderLines, Orders
from orderapp.models.bills import Bills
from orderapp.serializers.order_line import OrderLineSerializer
from commonapp.serializers.company import CompanySerializer
from userapp.models import User
from userapp.models.customer import Customer
from helpers.validators import phone_number_validator, is_numeric_value
from helpers.constants import MAX_LENGTHS, DEFAULTS
from django.db.models import Sum


class TableOrderOrderlineUpdateSerializer(CustomBaseSerializer):
    line_status = serializers.ChoiceField(ORDER_LINE_STATUS)

    class Meta:
        model = Orders
        field = ('line_status')
    
    def validate(self, attrs):
        # if not attrs.get('payment_mode') and attrs['status'] == ORDER_STATUS['COMPLETED']:
        #     raise ValidationError('Please enter payment mode')
        status = attrs['line_status']
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
        line_status = validated_data.get('line_status')
        request = self.context.get('request')
        types = request.query_params.get('types', None)
        if types:
            for lines in instance.lines.all():
                if lines.product.product_category.types == types:
                    lines.update(status = line_status)
                    lines.save()
        else:
            for lines in instance.lines.all():
                lines.update(status = line_status)
                lines.save()
        instance.save()
        return instance

class TableSalesSerializer(CustomBaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(required=False)
    asset_type = serializers.ChoiceField(choices=ASSET_TYPE_CHOICES)
    number_of_sales = serializers.IntegerField(max_value=None, min_value=None)
    total_amount = serializers.DecimalField(max_digits=20, decimal_places=6)



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
    payment_mode = serializers.ChoiceField(PAYMENT_CHOICES, required=False)
    custom_discount_percentage = serializers.CharField(validators=[is_numeric_value, is_percentage], required=False)
    voucher = DetailRelatedField(model=Voucher, lookup='id',
                                 representation='to_representation', required=False)
    paid_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=False)

    class Meta:
        model = Orders
        fields = ('status', 'payment_mode', 'custom_discount_percentage', 'custom_discount_amount', 'is_service_charge', 'voucher','paid_amount')

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
            for line in instance.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED']):
                line.update(voucher=voucher)
        order = Orders.execute_change_status(order=instance, v_data=validated_data, request=request)
        return order


class CompanyTableOrderSerializer(CustomModelSerializer):
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation', required=False)
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', required=False,\
                                read_only=True)
    takeaway = DetailRelatedField(model=DeliveryPartner, lookup='id', representation='to_representation', required=False)
    voucher = DetailRelatedField(model=Voucher, lookup='id', representation='to_representation',
                                 required=False, allow_null=True)
    order_lines = OrderLineSerializer(many=True, required=True)
    price_details = serializers.SerializerMethodField()
    user  = DetailRelatedField(model=User, lookup='id', representation='to_representation', read_only=True)
    bill = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('id', 'status', 'bill', 'company', 'voucher', 'is_service_charge', 'asset', 'order_lines', 'price_details', 'created_at', 'modified_at', 'user', 'takeaway')

    def get_bill(self, obj):
        try:
            obj.bills
        except Bills.DoesNotExist:
            return None
        return {'id': obj.bills.id, 'invoice_number': obj.bills.invoice_number, 'is_credit': obj.bills.is_credit, 'is_paid': obj.bills.is_paid,
                    'grand_total': obj.bills.get_grand_total(), 'subtotal': obj.bills.get_subtotal(), 'payment_mode': obj.bills.payment_mode,
                    'service_charge': obj.bills.service_charge if obj.bills.is_service_charge else 0, 'tax': obj.bills.tax}


    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        if request and request.method == 'GET': #or request.method=='PUT':
            fields['order_lines'] = serializers.SerializerMethodField('lines')
        return fields

    def lines(self, order):
        lines = OrderLineSerializer(order.lines.all(), many=True)
        return lines.data

    def get_price_details(self, obj):
        grand_total, tax_amount = obj.get_grand_total(obj)
        try:
            invoice_number = obj.bills.invoice_number
        except Bills.DoesNotExist:
            invoice_number = ''
        return {
            'invoice_number': invoice_number,
            'discount': obj.discount_amount,
            'sub_total': obj.subtotal,
            'tax': tax_amount,
            'service_charge': obj.service_charge_amount,
            'grand_total': grand_total,
            'custom_discount_percentage': obj.custom_discount_percentage,
            'custom_discount_amount': obj.custom_discount_amount
        }

    def validate(self, attrs):
        if self.instance:
            if hasattr(self.context['request'], 'company'):
                if self.context['request'].company != self.instance.company:
                    raise ValidationError('Cannot update for another company')
            else:
                if self.context['request'].parser_context['kwargs']['company_id'] != str(self.instance.company.id):
                    raise ValidationError('Cannot update for another company')
            if self.instance.status in [ORDER_STATUS['CANCELLED'], ORDER_STATUS['COMPLETED']]:
                raise ValidationError('Cannot update completed or cancelled order')
        elif 'asset' in attrs.keys():
            if attrs['asset'].orders.filter(status__in=[
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
        request = self.context.get('request')
        company = getattr(request, 'company', None)
        if not company:
            company = order.company
        if voucher and (voucher.coupon.company != company):
            raise ValidationError({'detail': 'voucher not found (voucher)'})
        for line in validated_order_line_data:
            new_quantity = int(line['quantity'])
            status = line.get('status', 'NEW')
            product = line['product']
            if str(product.company.id) != str(company.id):
                raise ValidationError({'detail': '{0} not found.'.format(product.name)})
            # if not status == ORDER_LINE_STATUS['CANCELLED']:
            order_line = OrderLines(order=order,
                                    product=product,
                                    status=status,
                                    new=line.get('new', 0),
                                    cooking=line.get('cooking', 0),
                                    served=line.get('served', 0),
                                    cancelled=line.get('cancelled', 0),
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
        user = self.context['request'].user
        validated_data['user'] = user
        if not validated_data['user'].is_authenticated:
            validated_data['user'] = None
        if voucher:
            validated_data['user'] = voucher.user
        validated_data['company'] = self.context['request'].company
        print(validated_data)
        order = super().create(validated_data)
        order_line_bulk_create_data = self.build_orderline_bulk_create_data(order, order_lines, voucher)
        OrderLines.objects.bulk_create(order_line_bulk_create_data)
        # if order.lines.exclude(status__in='SERVED').count() == 0:
        #     order.update(status=ORDER_STATUS['BILLABLE'])
        payable_amount, tax = self.get_grand_total(order)
        payable_amount = round(payable_amount, 6)
        order.payable_amount = payable_amount
        order.tax = tax
        order.service_charge = round(order.service_charge_amount,2)  if order.is_service_charge else 0
        order.save()
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
                notify_company_staffs(
                    company, NOTIFICATION_CATEGORY['ORDER_PLACED'], payload, asset=order.asset, exclude_user=user)
                pass
            except:
                pass
        return order

    def check_for_cancelled_order(self, order_lines):
        is_cancelled = True
        for line in order_lines:
            if not line.get('status') == ORDER_LINE_STATUS['CANCELLED'] or line.get('served')>0:
                is_cancelled = False
                break
        return is_cancelled

    @transaction.atomic
    def update(self, instance, validated_data):
        from notifications.tasks import notify_company_staffs
        asset = instance.asset 
        order_lines=None
        # print(self.context['request'].company)
        if 'order_lines' in validated_data:
            self.fields.pop('order_lines')
            self.fields.pop('voucher')
            order_lines = validated_data.pop('order_lines')

            is_cancelled = self.check_for_cancelled_order(order_lines)
            if is_cancelled:
                instance.delete()
                return instance
        voucher = validated_data.pop('voucher', None)
        user = self.context['request'].user
        validated_data['user'] = user
        if not validated_data['user'].is_authenticated:
            validated_data['user'] = None
        if voucher:
            validated_data['user'] = voucher.user
        validated_data['company'] = self.context['request'].company
        served_products = dict()
        # for line in instance.lines.exclude(status=ORDER_LINE_STATUS['CANCELLED']):
        for line in instance.lines.all():
            # if line.status == 'SERVED':
            #     served_products[str(line.product.id)] = line.quantity
            # else:
            line.delete(force_delete=True)
        if order_lines:
            order_line_bulk_create_data = self.build_orderline_bulk_create_data(instance, order_lines, voucher,
                                                                                served_products)
            OrderLines.objects.bulk_create(order_line_bulk_create_data)
        order = super().update(instance, validated_data)
        payable_amount, tax = self.get_grand_total(order)
        payable_amount = round(payable_amount, 6)
        order.payable_amount = payable_amount
        order.tax = tax
        order.service_charge = round(order.service_charge_amount,2)  if order.service_charge_amount else 0
        order.save()
        company = str(order.company.id)
        if order.asset:
            if order.asset == asset:
                message = 'Order has been updated at {0} {1}'.format(order.asset.asset_type, order.asset.name)
            else:
                if asset:
                    message = 'Order has been updated from {0} {1} to {2} {3}'.format(asset.asset_type, asset.name, order.asset.asset_type, order.asset.name)
                else:
                    message = 'Order has been updated to {0} {1}'.format(order.asset.asset_type, order.asset.name)        
        else:
            message = 'Order has been updated'
        payload = {
            'id': str(order.id),
            'category': NOTIFICATION_CATEGORY_NAME['ORDER_PLACED'],
            'message': {
                'en': message
            }
        }
        try:
            notify_company_staffs(
                company, NOTIFICATION_CATEGORY['ORDER_PLACED'], payload, asset=order.asset, exclude_user=user)
        except Exception as e:
            pass
        return order

    def get_grand_total(self, order):
        grand_total=0.0
        taxed_amount = order.company.tax if order.company.tax else 0
        service_charge_amount = order.company.service_charge if order.company.service_charge else 0
        total = float(order.lines.all().aggregate(order_total=Sum('total'))['order_total']) if order.lines.all().aggregate(order_total=Sum('total'))['order_total'] else 0
        print(total)
        grand_total = grand_total + total 
        service_charge_amount = float(service_charge_amount) / 100 * float(total) if order.is_service_charge else 0 #if is_service_charge else 0
        grand_total = grand_total + service_charge_amount
        discount_amount = self.get_discount_amount(order, grand_total) 
        grand_total = grand_total - discount_amount 
        taxed_amount = float(taxed_amount) / 100 * float(grand_total)
        taxed_amount = round(taxed_amount, 2)
        grand_total = round(grand_total + taxed_amount, 2)
        return (grand_total, taxed_amount)

    def get_discount_amount(self, order, grand_total):
        value = 0.0
        if order.custom_discount_percentage:
            custom_discount = float(order.custom_discount_percentage/100) * float(grand_total)
            value = value + custom_discount
        if order.custom_discount_amount:
            value = value + order.custom_discount_amount
        return value


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


class MasterQRSerializer(CompanyTableOrderSerializer):
    phone_number = serializers.CharField(required=False, allow_null=True)
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation', required=True)
    voucher = DetailRelatedField(model=Voucher, lookup='id', representation='to_representation',
                                 required=False, allow_null=True)
    order_lines = OrderLineSerializer(many=True, required=True)
    price_details = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('id', 'status', 'voucher', 'asset', 'order_lines', 'price_details', 'phone_number')

    @transaction.atomic
    def create(self, validated_data, notify=True):
        from notifications.tasks import notify_company_staffs
        self.fields.pop('order_lines')
        self.fields.pop('voucher')
        phone_number = self.fields.pop('phone_number')
        phone_number_user = User.objects.filter(phone_number=phone_number)
        company = validated_data['asset'].company
        order_lines = validated_data.pop('order_lines')
        voucher = validated_data.pop('voucher', None)
        validated_data['user'] = self.context['request'].user
        if not validated_data['user'].is_authenticated:
            validated_data['user'] = company.qr_user
        if voucher:
            validated_data['user'] = voucher.user if not phone_number_user else phone_number_user

        validated_data['company'] = company
        order = super(CompanyTableOrderSerializer, self).create(validated_data)

        order_line_bulk_create_data = self.build_orderline_bulk_create_data(order, order_lines, voucher)
        OrderLines.objects.bulk_create(order_line_bulk_create_data)
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
                notify_company_staffs(
                    company, NOTIFICATION_CATEGORY['ORDER_PLACED'], payload, asset=order.asset)
            except Exception as e:
                pass
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        from notifications.tasks import notify_company_staffs
        self.fields.pop('order_lines')
        self.fields.pop('voucher')
        order_lines = validated_data.pop('order_lines')

        is_cancelled = self.check_for_cancelled_order(order_lines)
        if is_cancelled:
            instance.delete()
            return instance
        voucher = validated_data.pop('voucher', None)
        validated_data['user'] = self.context['request'].user
        company = validated_data['asset'].company
        if not validated_data['user'].is_authenticated:
            validated_data['user'] = None
        if voucher:
            validated_data['user'] = voucher.user
        validated_data['company'] = company
        served_products = dict()
        for line in instance.lines.all():
            line.delete(force_delete=True)
        order_line_bulk_create_data = self.build_orderline_bulk_create_data(instance, order_lines, voucher,
                                                                            served_products)
        OrderLines.objects.bulk_create(order_line_bulk_create_data)
        order = super(CompanyTableOrderSerializer, self).update(instance, validated_data)
        company = str(order.company.id)
        if order.asset:
            message = 'Order has been updated from {0} {1}'.format(order.asset.asset_type, order.asset.name)
        else:
            message = 'An order has been updated'
        payload = {
            'id': str(order.id),
            'category': NOTIFICATION_CATEGORY_NAME['ORDER_PLACED'],
            'message': {
                'en': message
            }
        }
        try:
            notify_company_staffs(
                company, NOTIFICATION_CATEGORY['ORDER_PLACED'], payload, asset=order.asset)
        except Exception as e:
            pass
        return order
