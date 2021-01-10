from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from commonapp.models.coupon import Voucher
from commonapp.serializers.coupon import VoucherSerializer
from helpers.paginations import FPagination


class UserVoucherListAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Voucher.objects.all().order_by('-created_at')
    permission_classes = (IsAuthenticated, )
    serializer_class = VoucherSerializer
    pagination_class = FPagination

    def get_queryset(self):
        company_id = self.request.GET.get('company_id')
        return self.queryset.filter(user=self.request.user, is_redeem=False, coupon__company__id=company_id)
