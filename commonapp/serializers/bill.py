from rest_framework import serializers
from commonapp.models.bill import Bill
from commonapp.models.coupon import Voucher
from commonapp.models.salesitem import SalesItem
from commonapp.models.order import Order
from commonapp.serializers.coupon import VoucherSerializer
from commonapp.serializers.salesitem import SalesItemSerializer
from userapp.models.user import User

class BillSaveSerializer(serializers.ModelSerializer):
    sales = serializers.SerializerMethodField()
    sales_item = SalesItemSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = "__all__"
    
    def create(self, validated_data):
        sales_item_data = validated_data.pop('sales_item')
        bill_obj = Bill.objects.create(**validated_data)
        for sales_item in sales_item_data:
            sales_item_obj = SalesItem.objects.create(bill=bill_obj, **sales_item)
            if sales_item_obj.order:
                order_obj = Order.objects.filter(id=sales_item_obj.order_id)
                print(order_obj)
                if order_obj:
                    order_obj[0].is_billed = True
                    order_obj[0].save()
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
                SalesItem.objects.create(**sales_item)
        SalesItem.objects.filter(id__in=sales_item_ids).delete()
        bill_obj = Bill.objects.filter(id=instance.id).update(**validated_data)
        return bill_obj

    def get_sales(self, obj):
        print(obj)
        sales_item_obj = SalesItem.objects.filter(bill__id=obj.id)
        serializer = SalesItemSerializer(sales_item_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill=obj.id)
        total = 0
        for sales_item in sales_item_obj:
            total += sales_item.total
        return total

    def get_taxed_amount(self, obj):
        if obj.tax:
            total = self.get_total(obj)
            taxed_amount = obj.tax / 100 * total
        else:
            taxed_amount = 0
        return taxed_amount

    def get_grand_total(self, obj):
        return self.get_total(obj) + self.get_taxed_amount(obj)

class BillSerializer(serializers.ModelSerializer):
    sales_item = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

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
        return total

    def get_taxed_amount(self, obj):
        if obj.tax:
            total = self.get_total(obj)
            taxed_amount = obj.tax / 100 * total
        else:
            taxed_amount = 0
        return taxed_amount

    def get_grand_total(self, obj):
        return self.get_total(obj) + self.get_taxed_amount(obj)

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
        voucher_obj = Voucher.objects.filter(user=obj.id, coupon__company__id=company_id)
        serializer = VoucherSerializer(voucher_obj, many=True)
        return serializer.data