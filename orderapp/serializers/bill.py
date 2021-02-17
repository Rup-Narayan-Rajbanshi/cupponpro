from django.db import transaction
from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from helpers.constants import ORDER_STATUS, MAX_LENGTHS
from helpers.serializer import CustomModelSerializer
from orderapp.models.bills import Bills
from orderapp.models.order import Orders
from orderapp.serializers.order import CompanyTableOrderSerializer
from commonapp.models.company import Company
from userapp.models.customer import Customer
from userapp.serializers.user import UserDetailSerializer
from helpers.validators import phone_number_validator, is_numeric_value
from helpers.constants import DEFAULTS
from commonapp.models.asset import Asset
from rest_framework.exceptions import ValidationError
from orderapp.choice_variables import PAYMENT_CHOICES
from orderapp.serializers.transaction import TransactionHistoryBillSerializer
from django.db.models import Sum


class BillCreateSerializer(CustomModelSerializer):

    class Meta:
        model = Bills
        fields = "__all__"
    

    def create(self, validated_data):
        bill =  super(BillCreateSerializer, self).create(validated_data)
        data={
             'paid_amount' : float(bill.paid_amount) + float(bill.ret_amount),
             'return_amount': bill.ret_amount,
             'credit_amount': bill.credit_amount,
             'bill': bill.id
         }
        serializer = TransactionHistoryBillSerializer(data=data, context={'request': self.context['request']})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return bill

    def update(self, instance, validated_data):
        bill =  super(BillCreateSerializer, self).update(instance, validated_data)
        data={
             'paid_amount' : float(bill.paid_amount) + float(bill.ret_amount),
             'return_amount': bill.ret_amount,
             'credit_amount': bill.credit_amount,
             'bill': bill.id
         }
        serializer = TransactionHistoryBillSerializer(data=data, context={'request': self.context['request']})
        if serializer.is_valid():
            serializer.save()
        return bill

class BillListSerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation')
    order = serializers.SerializerMethodField()
    customer = DetailRelatedField(model=Customer, lookup='id', representation='to_representation', required=False)

    class Meta:
        model = Bills
        fields = "__all__"

    def get_order(self, obj):
        serializer_context = {'request': self.context.get('request')}
        serializer = CompanyTableOrderSerializer(obj.orders.all(), many=True, context=serializer_context)
        return serializer.data


class ManualBillSerializerCompany(CompanyTableOrderSerializer):
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation', allow_null=True, required=False)
    customer = DetailRelatedField(model=Customer, lookup='id', representation='to_representation', required=False)
    name = serializers.CharField(max_length=128, allow_blank=True, required=False)
    phone_number = serializers.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER'],
                                    validators=[phone_number_validator, is_numeric_value], allow_blank=True, required=False)
    email = serializers.EmailField(max_length=MAX_LENGTHS['EMAIL'], allow_blank=True, required=False)
    address = serializers.CharField(max_length=MAX_LENGTHS['ADDRESS'], allow_blank=True, required=False)
    payment_mode = serializers.ChoiceField(PAYMENT_CHOICES, required=False)
    paid_amount = serializers.DecimalField(max_digits=20, decimal_places=6, required=False)
    is_manual = serializers.BooleanField(required=False)

    class Meta(CompanyTableOrderSerializer.Meta):
        fields = list(CompanyTableOrderSerializer.Meta.fields) + ['payment_mode', 'paid_amount', 'is_manual','customer', 'name','phone_number', 'email', 'address']
        # fields = ('id', 'voucher', 'asset', 'order_lines', 'bill' ,'customer', 'name','phone_number', 'email', 'address')

    def validate(self, attrs):
        if self.instance:
            bill = self.instance.bill
            if bill.is_paid == "True":
                raise ValidationError({'message': 'Cannot change with is paid True.'})
        return super().validate(attrs)


    @transaction.atomic
    def create(self, validated_data):
        validated_data['status'] = ORDER_STATUS['BILLABLE']
        customer_data = dict()
        if 'name' in validated_data or 'phone_number' in validated_data:
            customer_data['name'] = validated_data.pop('name', '')
            customer_data['phone_number'] = validated_data.pop('phone_number', '')
            customer_data['email'] = validated_data.pop('email', '')
            customer_data['address'] = validated_data.pop('address', DEFAULTS['ADDRESS'])
        order = super().create(validated_data)
        customer = Customer.getcreate_customer(**customer_data)
        first_line = order.lines.first()
        data = dict()
        data['is_manual'] = True
        data['company'] = order.company.id
        data['tax'] = order.company.tax if order.company.tax else 0
        data['service_charge'] = order.company.service_charge if order.company.service_charge else 0
        data['customer'] = customer.id if customer else None
        data['payable_amount'] = self.get_grand_total(order) 
        data['paid_amount'] = validated_data['paid_amount'] if 'paid_amount' in validated_data else 0
        data['payment_mode'] = validated_data['payment_mode'] if 'payment_mode' in validated_data else 'CASH'
        serializer = BillCreateSerializer(data=data, context={'request': self.context['request']})
        if not serializer.is_valid():
            raise serializers.ValidationError(detail='Cannot bill the order', code=400)
        order.bill = serializer.save()
        order.save()
        if first_line and first_line.voucher:
            order.user = first_line.voucher.user
        return order
    
    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data['status'] = ORDER_STATUS['BILLABLE']
        customer_data = dict()
        if 'name' in validated_data or 'phone_number' in validated_data:
            customer_data['name'] = validated_data.pop('name', '')
            customer_data['phone_number'] = validated_data.pop('phone_number', '')
            customer_data['email'] = validated_data.pop('email', '')
            customer_data['address'] = validated_data.pop('address', DEFAULTS['ADDRESS'])
        order = super().update(instance, validated_data)
        customer = Customer.getcreate_customer(**customer_data)
        first_line = order.lines.first()
        data = dict()
        data['is_manual'] = validated_data['is_manual'] if 'is_manual' in validated_data else order.bill.is_manual
        data['company'] = order.company.id
        data['tax'] = order.company.tax if order.company.tax else 0
        data['service_charge'] = order.company.service_charge if order.company.service_charge else 0
        data['customer'] = customer.id if customer else None
        data['payment_mode'] = validated_data['payment_mode'] if 'payment_mode' in validated_data else order.bill.payment_mode
        data['paid_amount'] = validated_data['paid_amount'] if 'paid_amount' in validated_data else order.bill.paid_amount
        data['payable_amount'] = self.get_grand_total(order) 
        serializer = BillCreateSerializer(instance=order.bill, data=data, context={'request': self.context['request']})
        if not serializer.is_valid():
            raise serializers.ValidationError(detail='Cannot update bill. ', code=400)
        order.bill = serializer.save()
        order.save()
        if first_line and first_line.voucher:
            order.user = first_line.voucher.user
        return order

    def get_grand_total(self, order):
        grand_total=0.0
        taxed_amount = order.company.tax if order.company.tax else 0
        service_charge_amount = order.company.service_charge if order.company.service_charge else 0
        total = float(order.lines.aggregate(order_total=Sum('total'))['order_total']) if order.lines.aggregate(order_total=Sum('total'))['order_total'] else 0
        taxed_amount = float(taxed_amount) / 100 * float(total)
        service_charge_amount = float(service_charge_amount) / 100 * float(total) #if is_service_charge else 0
        grand_total = grand_total + total + taxed_amount + service_charge_amount
        return grand_total
