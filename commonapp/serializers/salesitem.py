from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from commonapp.models.salesitem import SalesItem
from commonapp.models.order import OrderLine


class SalesItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, allow_null=True)
    order = DetailRelatedField(model=OrderLine, lookup='id', representation='__str__')
    product_name = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = SalesItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_code(self, obj):
        return obj.product.product_code
