from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from helpers.validators import is_alphanumeric_with_exception
from helpers.serializer_fields import DetailRelatedField, LowertoUpperChoiceField, CouponContentTypeField
from helpers.serializer import CustomModelSerializer
from commonapp.models.coupon import Coupon
from commonapp.models.company import Company
from helpers.choices_variable import DISCOUNT_CHOICES
from commonapp.models.image import Image
from helpers.app_helpers import url_builder


class CouponSerializer(CustomModelSerializer):
    name = serializers.CharField(max_length=30, validators=[is_alphanumeric_with_exception,])
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', read_only=True)
    discount_type = LowertoUpperChoiceField(DISCOUNT_CHOICES)
    content_type = CouponContentTypeField(model=ContentType, lookup='model', representation='to_representation')
    content_object = serializers.SerializerMethodField()
    expiry_date = serializers.DateField(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta(CustomModelSerializer.Meta):
        model = Coupon

    def get_content_object(self, obj):
        content_object = None
        if obj.content_object:
            content_object = obj.content_object.to_represent_minimal()
        return content_object

    def get_images(self, obj):
        coupon_type = obj.content_type.name
        images = list()
        request = self.context.get('request')
        if coupon_type == 'category':
            if obj.company:
                logo = url_builder(obj.company.logo, request)
                images = [logo]
        elif coupon_type == 'product':
            images_query = Image.objects.filter(content_type__model=coupon_type, object_id=obj.object_id).values_list('image', flat=True)
            images = [url_builder(x, request) for x in images_query]
        elif coupon_type == 'product category':
            image = url_builder(obj.content_object.image, request)
            images = [image]
        return images


class DealOfDaySerializer(CouponSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Coupon
        fields= ('id', 'name', 'company', 'description', 'discount_type', 'discount', 'images', 'content_type', 'content_object')


class TrendingCouponSerializer(CouponSerializer):

    class Meta(CustomModelSerializer.Meta):
        model = Coupon
        fields= ('id', 'name', 'company', 'description', 'discount_type', 'discount', 'images', 'content_type', 'content_object')
