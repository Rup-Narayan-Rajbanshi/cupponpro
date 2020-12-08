from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from orderapp.models.order_scan_log import OrderScanLog
from orderapp.serializers.order_scan_log import ValidateOrderScanSerializer


class ValidateOrderScanAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = OrderScanLog.objects.all().order_by('-created_on')
    serializer_class = ValidateOrderScanSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = super(ValidateOrderScanAPI, self).create(request, *args, **kwargs)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
