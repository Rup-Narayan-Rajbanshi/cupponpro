from rest_framework import serializers
from commonapp.models.coupon import Coupon
from commonapp.serializers.image import ImageSerializer

class CouponSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Coupon
        fields = "__all__" 