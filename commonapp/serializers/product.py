from rest_framework import serializers
from commonapp.models.product import BulkQuantity, Product, ProductCategory
from commonapp.serializers.image import ImageDetailSerializer

class BulkQuantitySerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkQuantity
        fields = "__all__"

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    images = ImageDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__" 