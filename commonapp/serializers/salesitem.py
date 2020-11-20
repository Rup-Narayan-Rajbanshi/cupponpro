from commonapp.models.salesitem import SalesItem
from rest_framework import serializers

class SalesItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, allow_null=True)
    product_name = serializers.SerializerMethodField()
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = SalesItem
        fields = '__all__'

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_code(self, obj):
        return obj.product.product_code