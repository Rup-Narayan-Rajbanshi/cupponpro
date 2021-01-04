from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet, ViewSet
from rest_framework import generics, status

from commonapp.models.company import CompanyUser
from commonapp.models.coupon import Voucher
from commonapp.models.order import Order
from commonapp.models.product import Product
from commonapp.models.salesitem import SalesItem
from helpers.constants import ORDER_STATUS
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from orderapp.models.order import Orders
from permission import CompanyUserPermission, isCompanyManagerAndAllowAll
from orderapp.serializers.order import OrderStatusSerializer, TableOrderCreateSerializer, TableOrderSerializer


class OrderStatusAPI(FAPIMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderStatusSerializer
    permission_classes = (CompanyUserPermission, )


class OrderCountAPI(generics.GenericAPIView):
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    serializer_class = TableOrderSerializer
    pagination_class = FPagination

    def get(self, request):
        """
        An endpoint for getting order counts product detail.
        """
        company_user = CompanyUser.objects.filter(user=self.request.user)[0]
        qs = Orders.objects.filter(company_id=company_user.company.id)

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
    serializer_class = TableOrderSerializer
    permission_classes = (CompanyUserPermission, )


class CalculateOrderAPI(generics.GenericAPIView):
    permission_classes = (CompanyUserPermission, )
    serializer_class = TableOrderSerializer

    def post(self, request):
        response = dict()
        response['subtotal'] = 0.0
        response['grand_total'] = 0.0
        voucher = request.data['voucher']
        if voucher:
            voucher = Voucher.objects.filter(id=voucher).first()
        order_lines = request.data['order_lines']
        for line in order_lines:
            product = Product.objects.filter(company=request.company, id=line['product']).first()
            if not product:
                raise APIException('Cannot find product {}'.format(line['product']))
            response['subtotal'] = float(response['subtotal']) + float(product.get_line_subtotal(line['quantity'], voucher))
        response['tax'] = request.company.tax if request.company.tax else 0
        response['service_charge'] = request.company.service_charge if request.company.service_charge else 0
        taxed_amount = (response['tax']/100) * response['subtotal']
        response['grand_total'] = float(response['subtotal']) - response['service_charge'] - taxed_amount
        return Response(response, status=status.HTTP_200_OK)
