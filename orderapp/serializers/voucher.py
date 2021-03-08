from rest_framework import serializers

from productapp.models.coupon import Voucher, Coupon
from helpers.serializer import CustomModelSerializer
from helpers.serializer_fields import DetailRelatedField
from userapp.models import User


class VoucherListSerializer(CustomModelSerializer):
    coupon = DetailRelatedField(model=Coupon, lookup='id', representation='to_representation')
    used_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Voucher
        fields = ('id', 'is_redeem', 'used_date', 'coupon')

    def get_description(self, obj):
        return obj.coupon.description
