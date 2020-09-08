from rest_framework import serializers
from commonapp.models.coupon import Coupon
from commonapp.serializers.image import ImageSerializer

class CouponSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    coupon_relation = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        exclude = ('token', 'content_type')

    def get_coupon_relation(self, obj):
        return obj.content_object.__class__.__name__

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()

class VoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        exclude = ('token', )
    
    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()