from rest_framework import serializers
from commonapp.models.product import BulkQuantity, Product, ProductCategory
from commonapp.serializers.image import ImageDetailSerializer
from helpers.choices_variable import CURRENCY_TYPE_CHOICES, PRODUCT_STATUS_CHOICES


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
    purchase_currency = serializers.ChoiceField(CURRENCY_TYPE_CHOICES)
    selling_currency = serializers.ChoiceField(CURRENCY_TYPE_CHOICES)
    status = serializers.ChoiceField(PRODUCT_STATUS_CHOICES)

    class Meta:
        model = Product
        fields = "__all__"
