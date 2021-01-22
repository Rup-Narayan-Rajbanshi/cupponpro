from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.serializers.coupon import VoucherSerializer
from helpers.paginations import FPagination


class UserVoucherListAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Voucher.objects.all().order_by('-created_at')
    permission_classes = (AllowAny, )
    serializer_class = VoucherSerializer
    pagination_class = FPagination

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user, is_redeem=False, coupon__company__id=company_id)
        else:
            phone_number = self.request.GET.get('phone_number')
            if phone_number:
                return self.queryset.none()
            else:
                return self.queryset.filter(user__phone_number=phone_number,
                                            is_redeem=False,
                                            coupon__company__id=company_id)
