from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from commonapp.models.asset import Asset
from commonapp.serializers.asset import AssetSerializer
from helpers.api_mixins import FAPIMixin
from helpers.constants import ORDER_STATUS, ORDER_LINE_STATUS
from permission import isCompanyManagerAndAllowAll, CompanyUserPermission


class AssetFilter(filters.FilterSet):
    order_status = filters.CharFilter(field_name='company__order__status', exclude=True)

    class Meta:
        model = Asset
        fields = ['asset_type', 'order_status']

    def get_pending_tables(self, qs, all_served=True):
        qs = qs.filter(orders__status__in=[
            ORDER_STATUS['PROCESSING'], ORDER_STATUS['BILLABLE']])
        pending = []
        for asset in qs:
            latest_order = asset.orders.order_by('-created_at').first()
            if latest_order.lines.filter(
                status=ORDER_LINE_STATUS['SERVED']
            ).count() == latest_order.lines.count():
                pending.append(asset.id)

        if all_served:
            qs = qs.filter(id__in=pending)
        else:
            qs = qs.exclude(id__in=pending)
        return qs

    @property
    def qs(self):
        qs = super(AssetFilter, self).qs
        order_status = self.request.GET.get('order_status')
        if order_status == 'ACTIVE':
            pending_orders = self.get_pending_tables(qs, all_served=False)
            qs = qs.filter(orders__status__in=[ORDER_STATUS['NEW_ORDER'], ORDER_STATUS['CONFIRMED']])
            qs = qs | pending_orders
        elif order_status == 'PENDING_PAYMENT':
            qs = self.get_pending_tables(qs)
        return qs.distinct()


class AssetListAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    # queryset = Asset.objects.filter(asset_type=ASSET_TYPE['TABLE']).order_by('-created_at')
    queryset = Asset.objects.filter().order_by('-created_at')
    serializer_class = AssetSerializer
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    filter_backends = (DjangoFilterBackend,)
    filter_class = AssetFilter

    # pagination_class = FPagination

    def get_queryset(self):
        return self.queryset.filter(company_id=self.request.company)
