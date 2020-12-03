from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from notifications.models import (
    Notification,
    Device
)
from notifications.serializers import (
    NotificationSerializer,
    DeviceSerializer
)
from helpers.api_mixins import FAPIMixin
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from notifications.filters import (
    NotificationFilter,
    DeviceAdminFilter
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes
)
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import APIException


class NotificationAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Notification.objects.select_related('user').all()
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = FPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = NotificationFilter

    def list(self, request, *args, **kwargs):
        return super(NotificationAPI, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(NotificationAPI, self).retrieve(request, *args, **kwargs)


class DeviceAdminAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Device.objects.select_related('user').all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filter_class = DeviceAdminFilter

    def list(self, request, *args, **kwargs):
        return super(DeviceAdminAPI, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(DeviceAdminAPI, self).retrieve(request, *args, **kwargs)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated,))
def register_device(request):
    try:
        s = DeviceSerializer(data=request.data, context={'user': request.user})
        if s.is_valid():
            s.save()
            return Response(data={"detail": "Registered."}, status=200)
        else:
            return Response(data=s.errors, status=400)
    except Exception as e:
        print(str(e))
        raise APIException(detail=str(e), code=500)


@api_view(["PUT"])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated,))
def notification_seen(request, notification_id=None):
    notification = None
    try:
        if notification_id:
            notification = Notification.objects.get(id=notification_id, user=request.user)
    except Exception as e:
        return Response({"detail": "Object does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if notification:
            notification.mark_seen()
        else:
            Notification.objects.filter(user=request.user).update(seen=True)
    return Response({"detail": "Successfully marked as seen."}, status=status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([JSONRenderer])
@permission_classes((IsAuthenticated,))
def notification_unread_count(request):
    notification_count = Notification.count_unread(request.user)
    return Response({"unread": notification_count}, status=status.HTTP_200_OK)
