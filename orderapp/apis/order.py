from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from rest_framework import generics, status

from commonapp.models.company import CompanyUser
from commonapp.models.coupon import Voucher
from commonapp.models.order import Order
from commonapp.models.product import Product
from helpers.constants import ORDER_STATUS
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from orderapp.models.bills import Bills
from orderapp.models.order import Orders
from permission import CompanyUserPermission, isCompanyManagerAndAllowAll, isUser
from orderapp.serializers.order import OrderStatusSerializer, CompanyTableOrderSerializer, TableOrderSerializer, \
    UserOrderSerializerCompany, MasterQRSerializer


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
            "total_sales": Bills.objects.filter(company=company_user.company).count()
        }
        return Response(data, status=200)


class TableOrderAPI(ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [CompanyUserPermission]
    serializer_class = CompanyTableOrderSerializer
    pagination_class = FPagination

    def create(self, request, *args, **kwargs):
        created_response = super().create(request, *args, **kwargs)
        return Response(created_response.data, status=200)


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
        response['voucher'] = request.data.get('voucher', 0)
        if response['voucher']:
            voucher = Voucher.objects.filter(id=response['voucher']).first()
            response['discount'] = voucher.coupon.discount
            response['discount_type'] = voucher.coupon.discount_type
        order_lines = request.data['order_lines']
        for line in order_lines:
            product = Product.objects.filter(company=request.company, id=line['product']).first()
            if not product:
                raise APIException('Cannot find product {}'.format(line['product']))
            response['subtotal'] = float(response['subtotal']) + float(product.get_line_subtotal(line['quantity'], voucher))
        response['tax'] = request.company.tax if request.company.tax else 0
        response['service_charge'] = request.company.service_charge if request.company.service_charge else 0
        taxed_amount = (response['tax']/100) * response['subtotal']
        response['grand_total'] = float(response['subtotal']) + float(response['service_charge']) + float(taxed_amount)
        if response.get('discount_type', None) == 'PERCENTAGE':
            response['grand_total'] = response['grand_total'] - (float(response['discount']/100) * response['grand_total'])
        else:
            response['grand_total'] = response['grand_total'] - float(response['discount'])
        return Response(response, status=status.HTTP_200_OK)


class UserOrderListAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, )
    serializer_class = CompanyTableOrderSerializer
    pagination_class = FPagination

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status == 'ACTIVE':
            return self.queryset.filter(user=self.request.user,
                                        status__in=[
                                            ORDER_STATUS['NEW_ORDER'], ORDER_STATUS['CONFIRMED'],
                                            ORDER_STATUS['PROCESSING'], ORDER_STATUS['BILLABLE']])
        return self.queryset.filter(user=self.request.user)


class CustomerOrderAPI(ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [isUser]
    serializer_class = UserOrderSerializerCompany
    pagination_class = FPagination

    def create(self, request, *args, **kwargs):
        created_response = super().create(request, *args, **kwargs)
        return Response(created_response.data, status=200)


class MasterQROrderAPI(ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MasterQRSerializer
    pagination_class = FPagination

