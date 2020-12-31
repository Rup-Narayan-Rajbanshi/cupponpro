from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from commonapp.models.asset import Asset
from commonapp.models.company import CompanyUser
from commonapp.models.order import Order
from commonapp.serializers.asset import AssetSerializer
from helpers.api_mixins import FAPIMixin
from helpers.constants import ASSET_TYPE, ORDER_STATUS
from helpers.paginations import FPagination
from orderapp.models.order import Orders
from permission import isCompanyManagerAndAllowAll, CompanyUserPermission


class TableFilter(filters.FilterSet):
    order_status = filters.CharFilter(field_name='company__order__status', exclude=True)

    class Meta:
        model = Asset
        fields = ['asset_type', 'order_status']

    @property
    def qs(self):
        qs = super(TableFilter, self).qs
        order_status = self.request.GET.get('order_status')
        if order_status == 'ACTIVE':
            order_id_list = list(Orders.objects.filter(status__in=[
                ORDER_STATUS['NEW_ORDER'],
                ORDER_STATUS['CONFIRMED']]).values_list('id', flat=True))
            qs = qs.filter(company__orders__id__in=order_id_list)
        elif order_status == 'PENDING_PAYMENT':
            order_id_list = list(Orders.objects.filter(status__in=[
                ORDER_STATUS['PROCESSING']]).values_list('id', flat=True))
            qs = qs.filter(company__orders__id__in=order_id_list)
        return qs


class TableListAPI(FAPIMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Asset.objects.filter(asset_type=ASSET_TYPE['TABLE']).order_by('-created_at')
    serializer_class = AssetSerializer
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    filter_backends = (DjangoFilterBackend,)
    filter_class = TableFilter

    pagination_class = FPagination

    def get_queryset(self):
        company_user = CompanyUser.objects.filter(user=self.request.user)[0]
        return self.queryset.filter(company_id=company_user.company.id)
