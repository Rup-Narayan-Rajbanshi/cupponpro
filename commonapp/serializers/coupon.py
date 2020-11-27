from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import DetailRelatedField
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.image import Image
from userapp.models import User
from helpers.serializer_fields import LowertoUpperChoiceField, CouponContentTypeField
from helpers.constants import DISCOUNT_TYPE
from helpers.choices_variable import DISCOUNT_CHOICES


class CouponSerializer(serializers.ModelSerializer):
    discount_type = LowertoUpperChoiceField(DISCOUNT_CHOICES)
    content_type = CouponContentTypeField(model=ContentType, lookup='model', representation='to_representation')

    class Meta:
        model = Coupon
        fields = "__all__"

    def validate(self, attrs):
        content_type = attrs.get('content_type')
        object_id = attrs.get('object_id')
        content_class = content_type.model_class()
        try:
            object = content_class.objects.get(id=object_id)
        except ObjectDoesNotExist:
            raise ValidationError({'object_id': 'Object does not exist.'})
        return attrs

class CouponDetailSerializer(CouponSerializer):
    images = serializers.SerializerMethodField()
    coupon_relation = serializers.SerializerMethodField()
    is_redeemed = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    expiry_date = serializers.DateField(read_only=True)
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ('id', 'name', 'images', 'is_redeemed', 'description', 'discount_type', 'discount', 'coupon_relation', 'vendor', 'expiry_date', 'content_type', 'content_object')

    def get_content_object(self, obj):
        content_object = None
        if obj.content_object:
            content_object = obj.content_object.to_representation()
        return content_object

    def get_images(self, obj):
        coupon_type = obj.content_type.name
        current_site = Site.objects.get_current()
        if coupon_type == 'category':
            try:
                logo = current_site.domain + obj.company.logo.url
                logo = [logo]
            except:
                logo = None
            images = logo
        if coupon_type == 'product':
            content_type_obj = ContentType.objects.get(model='product')
            image_obj = Image.objects.filter(content_type=content_type_obj, object_id=obj.object_id)
            images = [current_site.domain + x.image.url for x in image_obj]
        if coupon_type == 'product category':
            try:
                image = current_site.domain + obj.company.logo.url
                image = [image]
            except:
                image = None
            images = image
        return images

    def get_coupon_relation(self, obj):
        return obj.content_object.__class__.__name__

    def get_is_redeemed(self, obj):
        if self.context.get('request').user and self.context.get('request').user.is_authenticated:
            user = self.context.get('request').user
            voucher_obj = Voucher.objects.filter(coupon=obj.id, user=user)
            if voucher_obj:
                return True
        return False

    # def get_vendor(self, obj):
    #     current_site = Site.objects.get_current()
    #     try:
    #         logo = current_site.domain + obj.company.logo.url
    #     except:
    #         logo = None
    #     if obj.company:
    #         company_id = obj.company.id
    #         company_name = obj.company.name
    #     else:
    #         company_id = None
    #         company_name = None
    #     if obj.company and obj.company.author:
    #         owner_id = obj.company.author.id
    #         owner_name = obj.company.author.full_name
    #         profile_image = current_site.domain + obj.company.author.image.url
    #     else:
    #         owner_id = None
    #         owner_name = None
    #         profile_image = None
    #     data = {
    #         'id': company_id,
    #         'name': company_name,
    #         'logo': logo,
    #         'owner_id': owner_id,
    #         'owner_name': owner_name,
    #         'profile_image': profile_image
    #     }
    #     return data

    def get_vendor(self, obj):
        company = obj.company.to_representation() if obj.company else dict()
        data = {
            'owner_id': None,
            'owner_name': None,
            'profile_image': None
        }
        if obj.company and obj.company.author:
            from helpers.app_helpers import url_builder
            owner_id = obj.company.author.id
            owner_name = obj.company.author.full_name
            profile_image = url_builder(obj.company.author.image, self.context.get('request'))
            data = {
                'owner_id': owner_id,
                'owner_name': owner_name,
                'profile_image': profile_image
            }
        company = {**company, **data}
        return company

class VoucherSerializer(serializers.ModelSerializer):
    coupon = DetailRelatedField(model=Coupon, lookup='id', representation='to_representation')
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation')
    description = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = ('id', 'is_redeem', 'used_date', 'description', 'coupon', 'user')

    def get_description(self, obj):
        return obj.coupon.description
