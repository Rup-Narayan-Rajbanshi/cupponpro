from rest_framework import serializers
from commonapp.models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_product_name(self, obj):
        return obj.product.name
