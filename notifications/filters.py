from notifications.models import (
    Notification,
    Device
)
from django_filters import rest_framework as filters


class NotificationFilter(filters.FilterSet):

    class Meta:
        model = Notification
        fields = ['seen', ]

    @property
    def qs(self):
        parent = super(NotificationFilter, self).qs
        user = getattr(self.request, 'user', None)
        return parent.filter(user=user)


class DeviceAdminFilter(filters.FilterSet):

    class Meta:
        model = Device
        fields = ['user__id']

    @property
    def qs(self):
        parent = super(DeviceAdminFilter, self).qs
        user = getattr(self.request, 'user', None)
        return parent.filter(user__owner=user.owner)
