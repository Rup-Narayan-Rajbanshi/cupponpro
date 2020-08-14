from rest_framework import serializers
from commonapp.models.coupon import Coupon

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = "__all__" 