from rest_framework import serializers
from commonapp.models.coupon import Coupon, Voucher
from commonapp.serializers.image import ImageSerializer

class CouponSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    coupon_relation = serializers.SerializerMethodField()
    is_redeemed = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ('token', 'content_type')

    def get_coupon_relation(self, obj):
        return obj.content_object.__class__.__name__

    def get_is_redeemed(self, obj):
        user = self.context.get('request').user
        voucher_obj = Voucher.objects.filter(coupon=obj.id, user=user)
        if voucher_obj:
            return True
        else:
            return False

class VoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voucher
        exclude = ('token', )