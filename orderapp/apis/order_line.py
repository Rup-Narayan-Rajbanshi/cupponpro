from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from helpers.api_mixins import FAPIMixin
from orderapp.models.order import OrderLines
from orderapp.serializers.order_line import OrderLineUpdateSerializer
from permission import CompanyUserPermission


class OrderLineAPI(FAPIMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = OrderLines.objects.all().order_by('-created_at')
    serializer_class = OrderLineUpdateSerializer
    permission_classes = (CompanyUserPermission, )

    def perform_destroy(self, instance):
        super(FAPIMixin, self).perform_destroy(instance)
