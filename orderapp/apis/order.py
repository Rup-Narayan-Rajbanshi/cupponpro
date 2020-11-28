from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from permission import CompanyUserPermission
from commonapp.models.order import Order
from orderapp.serializers.order import OrderStatusSerializer


class OrderStatusAPI(FAPIMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderStatusSerializer
    permission_classes = (CompanyUserPermission, )
