from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from helpers.constants import COUPON_TYPE_DISPLAY_MAPPER
from commonapp.models.coupon import Coupon
from productapp.serializers.coupon import DealOfDaySerializer, TrendingCouponSerializer, RecentCouponSerializer
from productapp.filters import DealOfDayFilter, TrendingCouponFilter, RecentCouponFilter


'''
Mapper to get coupon type
'''
class CouponTypeListView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        coupon_type = list()
        for key, value in COUPON_TYPE_DISPLAY_MAPPER.items():
            coupon_type.append({'key': key, 'name': value})
        data = {
            'success': 1,
            'data': coupon_type
        }
        return Response(data, status=200)


class DealOfDayAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Coupon.objects.select_related('company', 'content_type').all()
    serializer_class = DealOfDaySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = DealOfDayFilter
    pagination_class = FPagination
    permission_classes = (AllowAny, )


class TrendingCouponAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Coupon.objects.select_related('company', 'content_type').all()
    serializer_class = TrendingCouponSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TrendingCouponFilter
    pagination_class = FPagination
    permission_classes = (AllowAny, )


class RecentCouponAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Coupon.objects.select_related('company', 'content_type').all()
    serializer_class = RecentCouponSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecentCouponFilter
    pagination_class = FPagination
    permission_classes = (AllowAny, )
