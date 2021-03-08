from rest_framework import mixins
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from productapp.models.coupon import Voucher
from helpers.api_mixins import FAPIMixin
from helpers.paginations import FPagination
from orderapp.serializers.voucher import VoucherListSerializer
from permission import CompanyUserPermission, isUser


class VoucherListAPI(FAPIMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Voucher.objects.all().order_by('-created_at')
    serializer_class = VoucherListSerializer
    permission_classes = (CompanyUserPermission, )

    def get_queryset(self):
        phone_number = self.request.GET.get('phone_number')
        if not phone_number:
            raise APIException('Phone number is required')
        return self.queryset.filter(
            is_redeem=False,
            coupon__company=self.request.company,
            user__phone_number=phone_number)


class CustomerVoucherAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Voucher.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = VoucherListSerializer
    pagination_class = FPagination

    def get_queryset(self):
        is_redeem = self.request.query_params.get('is_redeem', False)
        qs1 = self.queryset.filter(
            is_redeem=is_redeem,
            user=self.request.user)   
        return qs1
