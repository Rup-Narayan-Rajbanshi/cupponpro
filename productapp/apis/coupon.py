from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from helpers.constants import COUPON_TYPE_DISPLAY_MAPPER
from django.db.models import Q, Max, Min
from django.utils import timezone

from productapp.filters import HighestDiscountCouponFilter
from productapp.models.coupon import Coupon
from productapp.models.product  import Product, ProductCategory
from productapp.filters import GlobalCouponFilter
from productapp.serializers.coupon import (
    DealOfDaySerializer,
    TrendingCouponSerializer,
    RecentCouponSerializer,
    LocalBusinessCouponSerializer,
    CouponSerializer
)
from productapp.filters import (
    DealOfDayFilter,
    TrendingCouponFilter,
    RecentCouponFilter,
    LocalBusinessCouponFilter
)


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


class LocalBusinessCouponAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Coupon.objects.select_related('company', 'content_type').all()
    serializer_class = LocalBusinessCouponSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = LocalBusinessCouponFilter
    pagination_class = FPagination
    permission_classes = (AllowAny, )


class GlobalSearchCouponAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filter_class = GlobalCouponFilter
    pagination_class = FPagination
    permission_classes = [AllowAny ]


class RelatedCouponCategoryAPI(generics.GenericAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        data=dict()
        q = request.GET.get('q','')

        related_company_dict = dict()
        discount_range = dict()

        product_obj_ids = Product.objects.filter(tag__icontains=q).values_list('id',flat=True)
        category_obj_ids = ProductCategory.objects.filter(tag__icontains=q).values_list('id',flat=True)
        global_search_coupon = Coupon.objects.filter(Q(company__name__icontains=q)|
                                                    Q(object_id__in=product_obj_ids)|
                                                    Q(object_id__in=category_obj_ids)
                                                    )

        companies = set([coupon.company for coupon in global_search_coupon])
        
        related_company_dict = [{'id':company.id,'name':company.name} for company in companies]

        coupons_object_ids = global_search_coupon.values_list('object_id',flat=True)

        related_category_dict = ProductCategory.objects.filter(id__in=coupons_object_ids).values('id', 'name')

        discount = global_search_coupon.filter(expiry_date__gte=timezone.now()).aggregate(Max('discount'),Min('discount'))
        discount_range['max'] = discount['discount__max']
        discount_range['min'] = discount['discount__min']

        data = {
            'success': 1,
            'category':related_category_dict,
            'companies': related_company_dict,
            'max_discount': discount_range
        }

        return Response(data, status=200)


class SpecialCouponAPI(mixins.ListModelMixin, GenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filter_class = HighestDiscountCouponFilter
    permission_classes = [AllowAny ]


class TagsAPI(generics.GenericAPIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        data=dict()
        q = request.GET.get('q','')

        product_tags = Product.objects.filter(tag__icontains=q).values_list('tag',flat=True).distinct()
        product_tags = ' '.join([str(elem) for elem in product_tags])
        product_tags = product_tags.replace(","," ")

        product_category_tags = ProductCategory.objects.filter(tag__icontains=q).values_list('tag',flat=True).distinct()
        product_category_tags = ' '.join([str(elem) for elem in product_category_tags])
        product_category_tags = product_category_tags.replace(","," ")
        
        tags = product_tags + " " + product_category_tags
        tags = tags.split(" ")
        tags = set([tag.strip() for tag in tags if tag])
        # tags = set([tag.strip() for tag in tags])

        tag_list = filter(lambda a: q.title() in a.title(), tags)
        data['tags'] = list(sorted(tag_list, key = len))[:10]

        return Response(data, status=200)