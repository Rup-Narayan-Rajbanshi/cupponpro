from rest_framework import serializers

from commonapp.models.product import Product
from helpers.choices_variable import ORDER_LINE_STATUS_CHOICES
from helpers.constants import ORDER_LINE_STATUS, ORDER_STATUS
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import DetailRelatedField
from orderapp.models.order import OrderLines, Orders
from rest_framework.exceptions import ValidationError

class OrderLineSerializer(CustomModelSerializer):
    product = DetailRelatedField(model=Product, lookup='id', representation='to_representation')
    quantity = serializers.CharField(required=True)
    total = serializers.CharField(required=False)
    new = serializers.IntegerField(required=False)
    cooking = serializers.IntegerField(required=False)
    served = serializers.IntegerField(required=False)
    cancelled = serializers.IntegerField(required=False)
    customer_comment = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = OrderLines
        fields = ['id', 'rate', 'quantity', 'status', 'discount_amount', 'total', 'product', 'new', 'cooking', 'served', 'cancelled','customer_comment',]

    def validate(self, attrs):
        if 'quantity' in attrs and int(attrs['quantity']) <= 0:
            raise ValidationError({"detail":"Quantity cannot be negative or zero. "})
        return attrs

class OrderLineUpdateSerializer(CustomModelSerializer):
    product = DetailRelatedField(model=Product, lookup='id', representation='to_representation')
    order = DetailRelatedField(model=Orders, lookup='id', representation='to_representation')
    quantity = serializers.IntegerField(required=True)
    total = serializers.CharField(required=False)

    class Meta:
        model = OrderLines
        fields = ['id', 'rate', 'quantity', 'status', 'discount_amount', 'total', 'product', 'order']

    def validate(self, attrs):
        if 'quantity' in attrs and int(attrs['quantity']) < 0:
            raise ValidationError({"detail":"Quantity cannot be negative. "})
        return attrs

    def create(self, validated_data):
        product = validated_data['product']
        validated_data['rate'] = float(product.total_price)
        line = validated_data['order'].lines.filter(product=product).first()
        if line:
            line.update(quantity=validated_data['quantity'])
            return line
        return super().create(validated_data)


class OrderLineStatusUpdate(CustomModelSerializer):
    status = serializers.ChoiceField(ORDER_LINE_STATUS_CHOICES)

    class Meta:
        model = OrderLines
        fields = ['id', 'status']

    def validate(self, attrs):
        status = attrs['status']
        allowed_status_change = {
            ORDER_LINE_STATUS['NEW']: [ORDER_LINE_STATUS['START_COOKING']],
            ORDER_LINE_STATUS['START_COOKING']: [ORDER_LINE_STATUS['SERVED']],
            ORDER_LINE_STATUS['SERVED']: [],
            ORDER_LINE_STATUS['CANCELLED']: []
        }

        if self.instance is not None:
            instance = self.instance
            if status not in allowed_status_change[instance.status]:
                raise serializers.ValidationError({'detail': 'Cannot change status from {} to {}.'.format(instance.status, status)})
        return attrs
