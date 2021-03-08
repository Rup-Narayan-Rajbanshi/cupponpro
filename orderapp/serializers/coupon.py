from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from productapp.models.coupon import Coupon
from userapp.models import User
from helpers.serializer_fields import LowertoUpperChoiceField, CouponContentTypeField
from helpers.constants import DISCOUNT_TYPE
from helpers.choices_variable import DISCOUNT_CHOICES



class CouponSerializer(serializers.ModelSerializer):
    discount_type = LowertoUpperChoiceField(DISCOUNT_CHOICES)
    content_type = CouponContentTypeField(model=ContentType, allow_null=True, lookup='model', representation='to_representation')

    class Meta:
        model = Coupon
        fields = "__all__"

    def validate(self, attrs):
        content_type = attrs.get('content_type')
        object_id = attrs.get('object_id')
        request = self.context.get('request')
        if request:
            try:
                company_user = request.user.company_user.all()
                company = company_user[0].company
            except:
                company = None
            if company:
                attrs['company'] = company
        
        if content_type and object_id:
            content_class = content_type.model_class()
            try:
                object = content_class.objects.get(id=object_id)
            except ObjectDoesNotExist:
                raise ValidationError({'object_id': 'Object does not exist.'})
        return attrs
