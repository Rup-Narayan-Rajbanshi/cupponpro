from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from productapp.models.product import BulkQuantity, Product, ProductCategory
from commonapp.serializers.image import ImageDetailSerializer
from helpers.choices_variable import CURRENCY_TYPE_CHOICES, PRODUCT_STATUS_CHOICES, PRODUCT_TYPE_CHOICES
from helpers.serializer import CustomModelSerializer

class BulkQuantitySerializer(CustomModelSerializer):

    class Meta:
        model = BulkQuantity
        fields = "__all__"

class ProductCategorySerializer(CustomModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)
    
    class Meta:
        model = ProductCategory
        fields = "__all__"

class ProductSerializer(CustomModelSerializer):
    images = ImageDetailSerializer(many=True, read_only=True)
    purchase_currency = serializers.ChoiceField(CURRENCY_TYPE_CHOICES)
    selling_currency = serializers.ChoiceField(CURRENCY_TYPE_CHOICES)
    status = serializers.ChoiceField(PRODUCT_STATUS_CHOICES)
    types = serializers.ChoiceField(PRODUCT_TYPE_CHOICES, allow_blank=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"
