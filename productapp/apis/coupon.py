from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from rest_framework.permissions import AllowAny
from helpers.api_mixins import FAPIMixin
from helpers.constants import COUPON_TYPE_MAPPER


'''
MApper to get coupon type
'''
class CouponTypeListView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        coupon_type = list()
        for key, value in COUPON_TYPE_MAPPER.items():
            coupon_type.append({'key': key, 'name': value})
        data = {
            'success': 1,
            'data': coupon_type
        }
        return Response(data, status=200)
