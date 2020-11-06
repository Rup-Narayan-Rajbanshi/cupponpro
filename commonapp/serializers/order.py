from rest_framework import serializers
from commonapp.models.order import OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = OrderLine
        fields = ['id', 'product', 'product_name', 'product_code', 'asset', 'rate', 'quantity', 'state']

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_code(self, obj):
        return obj.product.product_code