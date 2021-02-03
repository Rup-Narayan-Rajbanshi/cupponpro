from rest_framework import serializers
from helpers.choices_variable import PRODUCT_CAT_TYPE_CHOICES, PRODUCT_CAT_SUB_TYPE_CHOICES
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.product import ProductCategory
from commonapp.models.company import Company
from helpers.constants import DEFAULTS


class ProductCategorySerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation')
    image = ImageFieldWithURL(allow_empty_file=False)
    parent = DetailRelatedField(model=ProductCategory, lookup='id', representation='to_representation', allow_null=True, required=False)
    has_child = serializers.SerializerMethodField()
    types = serializers.ChoiceField(PRODUCT_CAT_TYPE_CHOICES)
    sub_type = serializers.ChoiceField(PRODUCT_CAT_SUB_TYPE_CHOICES, allow_blank=True, default=DEFAULTS['PRODUCT_CAT_SUB_TYPE'], required=False)

    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory

    def validate(self, attrs):
        request = self.context.get('request') 
        if request:
            if request.method == 'PUT':
                if 'parent' in attrs.keys():
                    if attrs['parent']!=None and self.instance.id == attrs['parent'].id:
                        raise serializers.ValidationError({'parent':'Product category cannot be parent of itself.'})
                    if 'types' not in attrs.keys():
                        if self.instance.types != attrs['parent']:
                            raise serializers.ValidationError({'parent': 'Type of sub category has to be same as its parent Product category.'})
                if self.instance.parent:
                    if 'types' in attrs.keys():
                        if self.instance.types != attrs['types']:
                            raise serializers.ValidationError({'types':'Type of sub category has to be same as its parent Product category.'})
            if ('parent' and 'types') in attrs.keys():
                if attrs['parent'].types != attrs['types']:
                        raise serializers.ValidationError({'parent':'Type of sub category has to be same as its parent Product category.'})
            if 'types' in attrs.keys():
                if attrs['types'] == 'BAR':
                    attrs['sub_type'] = ''
            company = request.company
            if company:
                attrs['company'] = company
        return super(ProductCategorySerializer, self).validate(attrs)

    def get_has_child(self, obj):
        has_child = ProductCategory.objects.filter(parent=obj).exists()
        return has_child
