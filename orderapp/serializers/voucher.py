from commonapp.models.coupon import Voucher
from helpers.serializer import CustomModelSerializer


class VoucherListSerializer(CustomModelSerializer):

    class Meta:
        model = Voucher
        fields = ('id', 'is_redeem', 'used_date', 'coupon', 'user')

    def get_description(self, obj):
        return obj.coupon.description
