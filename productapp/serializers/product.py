from rest_framework import serializers
from productapp.models.product import BulkQuantity, Product
from commonapp.serializers.image import ImageSerializer

class BulkQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkQuantity
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__" 