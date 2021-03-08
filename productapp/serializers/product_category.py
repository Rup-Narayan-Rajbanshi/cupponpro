from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.choices_variable import PRODUCT_CAT_TYPE_CHOICES
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import ImageFieldWithURL
from productapp.models.product import ProductCategory
from commonapp.models.company import Company
from helpers.constants import DEFAULTS, MAX_LENGTHS
from django.db.models import Max


class ProductSubCategorySerializer(CustomModelSerializer):
    
    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory
        fields = ['id','name', 'image','sub_type']


class ProductCategorySerializer(CustomModelSerializer):
    name = serializers.CharField(max_length=64, required=False)
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', required=False)
    image = ImageFieldWithURL(allow_empty_file=False, required=False)
    parent = DetailRelatedField(model=ProductCategory, lookup='id', representation='to_representation', allow_null=True, required=False)
    has_child = serializers.SerializerMethodField()
    child = serializers.SerializerMethodField()
    types = serializers.ChoiceField(PRODUCT_CAT_TYPE_CHOICES, allow_blank = True, required = False)
    sub_type = serializers.CharField(max_length=MAX_LENGTHS['PRODUCT_CAT_SUB_TYPE'], allow_blank=True, default=DEFAULTS['PRODUCT_CAT_SUB_TYPE'], required=False)

    class Meta(CustomModelSerializer.Meta):
        model = ProductCategory

    def validate(self, attrs):
        request = self.context.get('request')
        if request:
            company = getattr(request, 'company', None)
            if company:
                attrs['company'] = company
            name_exists_validation = 'Name "{0}" already exists.'.format(attrs.get('name', ''))
            # ## not clear
            if 'parent'in attrs.keys() and 'types' in attrs.keys():
                if attrs['parent']:
                    if attrs['parent'].types != attrs['types']:
                        raise serializers.ValidationError({'parent':'Type of sub category has to be same as its parent Product category.'})
            if self.instance:
                ## this is PUT
                if 'name' in attrs:
                    is_name_exists = ProductCategory.objects.exclude(id=self.instance.id).filter(company=attrs['company'], name=attrs['name']).exists()
                    if is_name_exists:
                        raise ValidationError({'name': name_exists_validation})
                if 'parent' in attrs.keys():
                    if attrs['parent']!=None and self.instance.id == attrs['parent'].id:
                        raise serializers.ValidationError({'parent':'Product category cannot be parent of itself.'})
                    if 'types' not in attrs.keys():
                        if self.instance.types != attrs['parent'].types:
                            raise serializers.ValidationError({'parent': 'Type of sub category has to be same as its parent Product category.'})
                if self.instance.parent:
                    if 'types' in attrs.keys():
                        if self.instance.types != attrs['types']:
                            raise serializers.ValidationError({'types':'Type of sub category has to be same as its parent Product category.'})
                if 'position' in attrs.keys():
                    self.rearrange_order(self.instance.position, attrs['position'])
            else:
                ## this is POST
                if 'name' in attrs:
                    is_name_exists = ProductCategory.objects.filter(company=attrs['company'], name=attrs['name']).exists()
                    if is_name_exists:
                        raise ValidationError({'name': name_exists_validation})
                if 'position' in attrs:
                    position_exist=ProductCategory.objects.filter(company=company,position=attrs['position'])
                    if position_exist:
                        raise ValidationError({'detail':'position already exists'})
                    # attrs['position'] = attrs['position']
                else:
                    last_position = ProductCategory.objects.filter(company=company).aggregate(Max('position'))
                    value_last_position = last_position['position__max']
                    attrs['position'] = value_last_position + 1
        return super(ProductCategorySerializer, self).validate(attrs)

    def get_has_child(self, obj):
        has_child = ProductCategory.objects.filter(parent=obj).exists()
        return has_child

    def get_child(self, obj):
        child = ProductCategory.objects.filter(parent=obj)
        serializer = ProductSubCategorySerializer(child,many=True)
        return serializer.data
    
    def rearrange_order(self, initial_position, final_position):
        change_order = initial_position - final_position
        if change_order > 0:
            models = ProductCategory.objects.filter(position__gte=final_position,position__lt=initial_position)
            for model in models:
                model.position += 1
                model.save()
        elif change_order < 0:
            models = ProductCategory.objects.filter(position__lte=final_position,position__gt=initial_position)
            for model in models:
                model.position -= 1
                model.save()
        else:
            pass
