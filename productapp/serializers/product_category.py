from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.product import ProductCategory
from commonapp.models.company import Company


class ProductCategorySerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation')
    image = ImageFieldWithURL(allow_empty_file=False)
    parent = DetailRelatedField(model=ProductCategory, lookup='id', representation='to_representation')
    has_child = serializers.SerializerMethodField()
    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            company = request.company
            if company:
                attrs['company'] = company
        return super(ProductCategorySerializer, self).validate(attrs)
    def get_has_child(self, obj):
        has_child = ProductCategory.objects.filter(parent=obj).exists()
        return has_child

