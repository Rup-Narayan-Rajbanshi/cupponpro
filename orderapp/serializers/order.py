from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import ImageFieldWithURL
from django.contrib.contenttypes.models import ContentType
from helpers.serializer import CustomModelSerializer
from helpers.constants import ORDER_STATUS
from helpers.choices_variable import ORDER_STATUS_CHOICES
from commonapp.models.order import Order


class OrderStatusSerializer(CustomModelSerializer):
    status = serializers.ChoiceField(ORDER_STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ('status', )

    def validate(self, attrs):
        status = attrs['status']
        allowed_status_change = {
            ORDER_STATUS['NEW_ORDER']: [ORDER_STATUS['CONFIRMED'], ORDER_STATUS['CANCELLED']],
            ORDER_STATUS['CONFIRMED']: [ORDER_STATUS['PROCESSING']],
            ORDER_STATUS['PROCESSING']: [ORDER_STATUS['BILLABLE']],
            ORDER_STATUS['BILLABLE']: [],
            ORDER_STATUS['CANCELLED']: []
        }

        if self.instance is not None:
            instance = self.instance
            if status not in allowed_status_change[instance.status]:
                raise ValidationError({'detail': 'Cannot change status from {} to {}.'.format(instance.status, status)})
        return attrs

    def update(self, instance, validated_data):
        request_user = self.context.get('request').user if self.context.get('request') else None
        order = Order.execute_change_status(order=instance, v_data=validated_data, request_user=request_user)
        return order
