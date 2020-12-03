from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from notifications.models import (
    Device,
    NotificationCategory,
    Notification

)
from userapp.models import User


class NotificationSerializer(CustomModelSerializer):
    category = DetailRelatedField(
        NotificationCategory,
        lookup='id',
        representation='to_representation'
    )
    user = DetailRelatedField(
        User,
        lookup='id',
        representation='to_representation'
    )

    class Meta(CustomModelSerializer.Meta):
        model = Notification


class DeviceSerializer(CustomModelSerializer):
    user = DetailRelatedField(
        User,
        lookup='id',
        representation='to_representation',
        read_only=True
    )

    class Meta(CustomModelSerializer.Meta):
        model = Device

    def create(self, data):
        data['user'] = self.context['user']
        return Device.update_or_create(**data)
