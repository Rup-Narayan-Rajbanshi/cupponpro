from rest_framework import serializers

from productapp.models.coupon import Voucher, Coupon
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import DetailRelatedField
from userapp.models import User
from productapp.serializers.coupon import CouponSerializer


class VoucherListSerializer(CustomModelSerializer):
    coupon = serializers.SerializerMethodField()
    used_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Voucher
        fields = ('id', 'is_redeem', 'used_date', 'coupon')

    def get_description(self, obj):
        return obj.coupon.description

    def get_coupon(self, obj):
        coupon = obj.coupon
        serializer = CouponSerializer(coupon, context={'request': self.context['request']})
        print(serializers)
        return serializer.data
