from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.choices_variable import PRODUCT_CAT_TYPE_CHOICES
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.product import ProductCategory, Product
from commonapp.serializers.product import ProductSerializer
from commonapp.models.company import Company
from helpers.constants import DEFAULTS, MAX_LENGTHS


class MenuSubCategorySerializer(CustomModelSerializer):
    product = serializers.SerializerMethodField()
    
    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory
        fields = ['id','name', 'image','sub_type', 'product']
    
    def get_product(self, obj):
        product = Product.objects.filter(product_category = obj)
        serializer = ProductSerializer(product, many=True)
        return serializer.data


class MenuSerializer(CustomModelSerializer):
    name = serializers.CharField(max_length=64, required=False)
    image = ImageFieldWithURL(allow_empty_file=False, required=False)
    parent = DetailRelatedField(model=ProductCategory, lookup='id', representation='to_representation', allow_null=True, required=False)
    has_child = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()
    types = serializers.ChoiceField(PRODUCT_CAT_TYPE_CHOICES, allow_blank = True, required = False)
    sub_type = serializers.CharField(max_length=MAX_LENGTHS['PRODUCT_CAT_SUB_TYPE'], allow_blank=True, default=DEFAULTS['PRODUCT_CAT_SUB_TYPE'], required=False)
    product = serializers.SerializerMethodField()

    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory
        field = ['name', 'image', 'parent', 'has_child', 'child', 'types', 'sub_types', 'product']

    def get_has_child(self, obj):
        has_child = ProductCategory.objects.filter(parent=obj).exists()
        return has_child

    def get_child(self, obj):
        child = ProductCategory.objects.filter(parent=obj)
        serializer = MenuSubCategorySerializer(child, many=True)
        return serializer.data

    def get_product(self, obj):
        if not self.get_has_child(obj):
            product = Product.objects.filter(product_category = obj)
            serializer = ProductSerializer(product, many=True)
            return serializer.data