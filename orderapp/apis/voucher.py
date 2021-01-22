from rest_framework import mixins
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from commonapp.models.coupon import Voucher
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
        qs = self.queryset.filter(
            is_redeem=False,
            user=self.request.user)
        company_id = self.request.GET.get('company_id')
        if company_id:
            qs = qs.filter(coupon__company__id=company_id)
        return qs
