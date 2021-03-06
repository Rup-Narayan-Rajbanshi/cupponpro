from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from commonapp.models.bill import Bill
from productapp.models.coupon import Voucher
from commonapp.models.salesitem import SalesItem
from commonapp.models.order import OrderLine
from commonapp.serializers.coupon import VoucherSerializer
from commonapp.serializers.salesitem import SalesItemSerializer
from userapp.models.user import User
from helpers.constants import ORDER_STATUS


class BillSaveSerializer(serializers.ModelSerializer):
    sales = serializers.SerializerMethodField()
    sales_item = SalesItemSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    service_charge = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = "__all__"

    def validate(self, attrs):
        sales_item_data = attrs.get('sales_item', [])
        orderline = None
        if len(sales_item_data) > 0:
            orderline = sales_item_data[0].get('order')
        if orderline:
            order = orderline.order
            if order.status != ORDER_STATUS['BILLABLE']:
                raise ValidationError({'detail': 'Cannot generate bill. Order status is not {0}'.format(ORDER_STATUS['BILLABLE'].lower())})
        return attrs

    def create(self, validated_data):
        sales_item_data = validated_data.pop('sales_item')
        bill_obj = Bill.objects.create(**validated_data)
        voucher_list = []
        for sales_item in sales_item_data:
            sales_item.pop('id', None)
            sales_item['bill'] = bill_obj
            sales_item_obj = SalesItem.objects.create(**sales_item)
            if sales_item_obj.voucher:
                if str(sales_item_obj.voucher.id) not in voucher_list:
                    voucher_list.append(str(sales_item_obj.voucher.id))
        Voucher.objects.filter(id__in=voucher_list).update(is_redeem=True, used_date=datetime.now())
        return bill_obj

    def update(self, instance, validated_data):
        sales_items = validated_data.pop('sales_item')
        sales_item_obj = SalesItem.objects.filter(bill=instance.id)
        sales_item_ids = [str(x.id) for x in sales_item_obj]
        for sales_item in sales_items:
            if sales_item['id']:
                SalesItem.objects.filter(id=sales_item['id']).update(**sales_item)
                sales_item_ids.remove(str(sales_item['id']))
            else:
                bill = sales_item.get('bill')
                if not bill:
                    sales_item['bill'] = instance
                SalesItem.objects.create(**sales_item)
        SalesItem.objects.filter(id__in=sales_item_ids).delete()
        bill_obj = Bill.objects.filter(id=instance.id).update(**validated_data)
        return bill_obj

    def get_sales(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill__id=obj.id)
        serializer = SalesItemSerializer(sales_item_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill=obj.id)
        total = 0
        for sales_item in sales_item_obj:
            total += sales_item.total
        return float(total)

    def get_taxed_amount(self, obj):
        if obj.tax:
            total = self.get_total(obj)
            taxed_amount = float(obj.tax) / 100 * total
        else:
            taxed_amount = 0
        return float(taxed_amount)

    def get_service_charge(self, obj):
        if obj.service_charge:
            total = self.get_total(obj)
            service_charge = float(obj.service_charge) / 100 * total
        else:
            service_charge = 0
        return float(service_charge)

    def get_grand_total(self, obj):
        return float(self.get_total(obj) + self.get_taxed_amount(obj) + self.get_service_charge(obj))

    def get_paid(self, obj):
        if obj.paid_amount:
            return float(obj.paid_amount) >= self.get_grand_total(obj)
        else:
            return False

class BillSerializer(serializers.ModelSerializer):
    sales_item = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    service_charge = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = "__all__"

    def get_sales_item(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill=obj.id)
        serializer = SalesItemSerializer(sales_item_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill=obj.id)
        total = 0
        for sales_item in sales_item_obj:
            total += sales_item.total
        return float(total)

    def get_taxed_amount(self, obj):
        if obj.tax:
            total = self.get_total(obj)
            taxed_amount = float(obj.tax) / 100 * total
        else:
            taxed_amount = 0
        return float(taxed_amount)

    def get_service_charge(self, obj):
        if obj.service_charge:
            total = self.get_total(obj)
            service_charge = float(obj.service_charge) / 100 * total
        else:
            service_charge = 0
        return float(service_charge)

    def get_grand_total(self, obj):
        return float(self.get_total(obj) + self.get_taxed_amount(obj) + self.get_service_charge(obj))

    def get_paid(self, obj):
        if obj.paid_amount:
            return float(obj.paid_amount) >= self.get_grand_total(obj)
        else:
            return False

class BillUserDetailSerializer(serializers.Serializer):
    """
    Serializer for getting billing user details.
    """
    model = User

    id = serializers.UUIDField(read_only=True)
    name = serializers.SerializerMethodField()
    voucher = serializers.SerializerMethodField()
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def get_name(self, obj):
        return obj.full_name

    def get_voucher(self, obj, **kwargs):
        company_id = self.context['request'].GET.get('company', None)
        voucher_obj = Voucher.objects.filter(user=obj.id, coupon__company__id=company_id, is_redeem=False)
        serializer = VoucherSerializer(voucher_obj, many=True)
        return serializer.data
