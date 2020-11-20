from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from rest_framework import serializers
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.image import Image


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class CouponDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    coupon_relation = serializers.SerializerMethodField()
    is_redeemed = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    expiry_date = serializers.DateField(read_only=True)
    content_type = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ('id', 'images', 'is_redeemed', 'description', 'discount', 'coupon_relation', 'vendor', 'expiry_date', 'content_type', 'content_object')

    def get_content_type(self, obj):
        content_type = obj.content_type.name
        return content_type

    def get_content_object(self, obj):
        content_object = None
        if obj.content_object:
            content_object = obj.content_object.to_representation()
        return content_object

    def get_images(self, obj):
        coupon_type = obj.content_type.name
        print(obj.id, coupon_type)
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

    def get_vendor(self, obj):
        current_site = Site.objects.get_current()
        try:
            logo = current_site.domain + obj.company.logo.url
        except:
            logo = None
        if obj.company:
            company_id = obj.company.id
            company_name = obj.company.name
        else:
            company_id = None
            company_name = None
        if obj.company and obj.company.author:
            owner_id = obj.company.author.id
            owner_name = obj.company.author.full_name
            profile_image = current_site.domain + obj.company.author.image.url
        else:
            owner_id = None
            owner_name = None
            profile_image = None
        data = {
            'id': company_id,
            'name': company_name,
            'logo': logo,
            'owner_id': owner_id,
            'owner_name': owner_name,
            'profile_image': profile_image
        }
        return data

class VoucherSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = ('id', 'is_redeem', 'used_date', 'description')

    def get_description(self, obj):
        return obj.coupon.description
