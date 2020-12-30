from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from rest_framework import generics

from commonapp.models.company import CompanyUser
from commonapp.models.order import Order
from commonapp.models.salesitem import SalesItem
from helpers.constants import ORDER_STATUS
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from orderapp.models.order import Orders
from permission import CompanyUserPermission, isCompanyManagerAndAllowAll
from orderapp.serializers.order import OrderStatusSerializer, TableOrderCreateSerializer, TableStatusChangeSerializer


class OrderStatusAPI(FAPIMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderStatusSerializer
    permission_classes = (CompanyUserPermission, )


class OrderCountAPI(generics.GenericAPIView):
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    serializer_class = OrderStatusSerializer
    pagination_class = FPagination

    def get(self, request):
        """
        An endpoint for getting order counts product detail.
        """
        company_user = CompanyUser.objects.filter(user=self.request.user)[0]
        qs = Order.objects.filter(company_id=company_user.company.id)

        data = {
            'success': 0,
            "active_orders": qs.filter(status=ORDER_STATUS['NEW_ORDER']).count(),
            "total_orders": qs.count(),
            "total_sales": SalesItem.objects.filter(product__company__id=company_user.company.id).count()
        }
        return Response(data, status=200)


class TableOrderAPI(ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [CompanyUserPermission]
    serializer_class = TableOrderCreateSerializer
    pagination_class = FPagination


class TableOrderStatusAPI(FAPIMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Orders.objects.all().order_by('-created_at')
    serializer_class = TableStatusChangeSerializer
    permission_classes = (CompanyUserPermission, )

