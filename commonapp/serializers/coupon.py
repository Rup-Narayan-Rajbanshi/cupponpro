from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from rest_framework import serializers
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.image import Image

class CouponSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    coupon_relation = serializers.SerializerMethodField()
    is_redeemed = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ('id', 'images', 'is_redeemed', 'description', 'discount', 'coupon_relation', 'vendor')

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
            image_obj = Image.objects.filter(content_type=content_type_obj, object_id=obj.id)
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
        data = {
            'name': obj.company.name,
            'logo': logo,
            'owner_name': obj.company.author.full_name,
            'profile_image': current_site.domain + obj.company.author.image.url
        }
        return data

class VoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voucher
        exclude = ('token', )