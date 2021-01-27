from rest_framework import serializers
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.product import ProductCategory
from commonapp.models.company import Company


class ProductCategorySerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation')
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            company = request.company
            if company:
                attrs['company'] = company
        return super(ProductCategorySerializer, self).validate(attrs)
    
