from rest_framework import serializers

from commonapp.models.product import Product
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import DetailRelatedField
from orderapp.models.order import OrderLines, Orders


class OrderLineSerializer(CustomModelSerializer):
    product = DetailRelatedField(model=Product, lookup='id', representation='to_representation')
    quantity = serializers.CharField(required=True)
    total = serializers.CharField(required=False)

    class Meta:
        model = OrderLines
        fields = ['id', 'rate', 'quantity', 'status', 'discount_amount', 'total', 'product']


class OrderLineUpdateSerializer(CustomModelSerializer):
    product = DetailRelatedField(model=Product, lookup='id', representation='to_representation')
    order = DetailRelatedField(model=Orders, lookup='id', representation='to_representation')
    quantity = serializers.IntegerField(required=True)
    total = serializers.CharField(required=False)

    class Meta:
        model = OrderLines
        fields = ['id', 'rate', 'quantity', 'status', 'discount_amount', 'total', 'product', 'order']

    def create(self, validated_data):
        product = validated_data['product']
        validated_data['rate'] = float(product.total_price)
        line = validated_data['order'].lines.filter(product=product).first()
        if line:
            line.update(quantity=validated_data['quantity'])
            return line
        return super().create(validated_data)
