from rest_framework import serializers
from commonapp.models.order import Order, OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, allow_null=True)
    product_name = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = OrderLine
        fields = ['id', 'product', 'product_name', 'product_code', 'rate', 'quantity','total','state', 'company', 'order']

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_code(self, obj):
        return obj.product.product_code

class OrderSaveSerializer(serializers.ModelSerializer):
    asset_name = serializers.SerializerMethodField()
    order = serializers.SerializerMethodField()
    order_lines = OrderLineSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
    
    def create(self, validated_data):
        order_lines_data = validated_data.pop('order_lines')
        order_obj = Order.objects.create(**validated_data)
        for order_lines in order_lines_data:
            OrderLine.objects.create(order=order_obj, **order_lines)  
        return order_obj

    def update(self, instance, validated_data):
        order_lines_data = validated_data.pop('order_lines')
        order_lines_obj = OrderLine.objects.filter(order=instance.id)
        order_lines_ids = [str(x.id) for x in order_lines_obj]
        for order_lines in order_lines_data:
            if order_lines['id']:
                OrderLine.objects.filter(id=order_lines['id']).update(**order_lines)
                order_lines_ids.remove(str(order_lines['id']))
            else:
                OrderLine.objects.create(**order_lines)
        OrderLine.objects.filter(id__in=order_lines_ids).delete()
        order_obj = Order.objects.filter(id=instance.id).update(**validated_data)
        return order_obj

    def get_asset_name(self, obj):
        return obj.asset.name

    def get_order(self, obj):
        order_lines_obj = OrderLine.objects.filter(order__id=obj.id)
        serializer = OrderLineSerializer(order_lines_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        order_lines_obj = OrderLine.objects.filter(order=obj.id)
        total = 0
        for order_lines in order_lines_obj:
            total += order_lines.total
        return float(total)

    def get_taxed_amount(self, obj):
        if obj.tax:
            total = self.get_total(obj)
            taxed_amount = obj.tax / 100 * total
        else:
            taxed_amount = 0
        return float(taxed_amount)

    def get_grand_total(self, obj):
        return float(self.get_total(obj) + self.get_taxed_amount(obj))

class OrderSerializer(serializers.ModelSerializer):
    asset_name = serializers.SerializerMethodField()
    order_lines = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    taxed_amount = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_asset_name(self, obj):
        return obj.asset.name

    def get_order_lines(self, obj):
        order_lines_obj = OrderLine.objects.filter(order__id=obj.id)
        serializer = OrderLineSerializer(order_lines_obj, many=True)
        return serializer.data

    def get_total(self, obj):
        order_lines_obj = OrderLine.objects.filter(order=obj.id)
        total = 0
        for order_lines in order_lines_obj:
            total += order_lines.total
        return float(total)

    def get_taxed_amount(self, obj):
        if obj.tax:
            total = self.get_total(obj)
            taxed_amount = obj.tax / 100 * total
        else:
            taxed_amount = 0
        return float(taxed_amount)

    def get_grand_total(self, obj):
        return float(self.get_total(obj) + self.get_taxed_amount(obj))