from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from productapp.models.coupon import Coupon
from helpers.api_mixins import FAPIMixin
from helpers.paginations import FPagination
from orderapp.filters import HighestDiscountCouponFilter
from orderapp.serializers.coupon import CouponSerializer


class SpecialCouponAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filter_class = HighestDiscountCouponFilter
    permission_classes = [AllowAny ]
