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

class BillCreateSerializer(CustomModelSerializer):

    class Meta:
        model = Bills
        fields = "__all__"

    def create(self, validated_data):
        return super(BillCreateSerializer, self).create(validated_data)

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
    customer = DetailRelatedField(model=Customer, lookup='id', representation='to_representation', required=False)
    name = serializers.CharField(max_length=128, allow_blank=True, required=False)
    phone_number = serializers.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER'],
                                    validators=[phone_number_validator, is_numeric_value], allow_blank=True, required=False)
    email = serializers.EmailField(max_length=MAX_LENGTHS['EMAIL'], allow_blank=True, required=False)
    address = serializers.CharField(max_length=MAX_LENGTHS['ADDRESS'], allow_blank=True, required=False)
    
    class Meta:
        model = Orders
        fields = ('id', 'voucher', 'asset', 'order_lines', 'bill' ,'customer', 'name','phone_number', 'email', 'address')

    @transaction.atomic
    def create(self, validated_data):
        validated_data['status'] = ORDER_STATUS['BILLABLE']
        customer_data = dict()
        if 'name' in validated_data.keys() or 'phone_number' in validated_data.keys():
            customer_data['name'] = validated_data.pop('name', '')
            customer_data['phone_number'] = validated_data.pop('phone_number', '')
            customer_data['email'] = validated_data.pop('email', '')
            customer_data['address'] = validated_data.pop('address', DEFAULTS['ADDRESS'])
        customer = Customer.getcreate_customer(**customer_data)
        order = super().create(validated_data)
        first_line = order.lines.first()
        data = dict()
        data['is_manual'] = True
        data['company'] = order.company.id
        data['tax'] = order.company.tax if order.company.tax else 0
        data['service_charge'] = order.company.service_charge if order.company.service_charge else 0
        data['customer'] = customer.id if customer else None
        serializer = BillCreateSerializer(data=data, context={'request': self.context['request']})
        if not serializer.is_valid():
            raise serializers.ValidationError(detail='Cannot bill the order', code=400)
        order.bill = serializer.save()
        if first_line and first_line.voucher:
            order.user = first_line.voucher.user
        return order
