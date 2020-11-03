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

    class Meta:
        model = Bill
        fields = "__all__"
    
    def create(self, validated_data):
        sales_item_data = validated_data.pop('sales_item')
        bill = Bill.objects.create(**validated_data)
        for sales_item in sales_item_data:
            sales_item_obj = SalesItem.objects.create(bill=bill, **sales_item)
            if sales_item_obj.order:
                order_obj = Order.objects.filter(id=sales_item_obj.order_id)
                print(order_obj)
                if order_obj:
                    order_obj[0].is_billed = True
                    order_obj[0].save()
        return bill

    def get_sales(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill=obj.id)
        serializer = SalesItemSerializer(sales_item_obj, many=True)
        return serializer.data

class BillSerializer(serializers.ModelSerializer):
    sales_item = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = "__all__"

    def get_sales_item(self, obj):
        sales_item_obj = SalesItem.objects.filter(bill=obj.id)
        serializer = SalesItemSerializer(sales_item_obj, many=True)
        return serializer.data

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