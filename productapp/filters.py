import math
from datetime import datetime
from django_filters import rest_framework as filters
from django.db.models import Q
from commonapp.models.image import Image
from commonapp.models.company import CompanyUser
from commonapp.models.product import Product, ProductCategory
from commonapp.models.coupon import Coupon


class ImageBaseFilter(filters.FilterSet):

    class Meta:
        model = Image
        fields = ['object_id']


class CompanyProductImageFilter(ImageBaseFilter):
    @property
    def qs(self):
        parent = super(CompanyProductImageFilter, self).qs
        company_user = CompanyUser.objects.select_related('company').filter(user=self.request.user).first()
        products = Product.objects.filter(company=company_user.company).values_list('id', flat=True)
        return parent.filter(content_type__model='product', object_id__in=products)


class CouponBaseFilter(filters.FilterSet):
    order = filters.CharFilter(field_name='company__id')
    name = filters.CharFilter(field_name='name__istartswith')

    class Meta:
        model = Coupon
        fields = ['name', 'company', 'object_id']


class DealOfDayFilter(CouponBaseFilter):
    @property
    def qs(self):
        parent = super(DealOfDayFilter, self).qs
        content_type = ['product', 'productcategory']
        return parent.filter(expiry_date__gt=datetime.now().date(),
                                content_type__model__in=content_type,
                                company__affilated_companies__isnull=False
                            )


class TrendingCouponFilter(CouponBaseFilter):
    @property
    def qs(self):
        parent = super(TrendingCouponFilter, self).qs
        content_type = ['productcategory']
        return parent.filter(expiry_date__gt=datetime.now().date(),
                                content_type__model__in=content_type,
                                company__affilated_companies__isnull=False
                            )


class RecentCouponFilter(CouponBaseFilter):
    @property
    def qs(self):
        parent = super(RecentCouponFilter, self).qs
        content_type = ['product']
        return parent.filter(expiry_date__gt=datetime.now().date(),
                                content_type__model__in=content_type,
                                company__affilated_companies__isnull=True
                            )


class LocalBusinessCouponFilter(CouponBaseFilter):

    def try_catch_get(self, key, default, type):
        value = default
        try:
            if type == 'float':
                value = float(self.request.GET.get(key, value))
            else:
                value = self.request.GET.get(key, value)
        except Exception as e:
            pass
        return value

    @property
    def qs(self):
        parent = super(LocalBusinessCouponFilter, self).qs
        latitude = self.try_catch_get('latitude', None, 'float')
        longitude = self.try_catch_get('longitude', None, 'float')
        distance = self.try_catch_get('distance', 5, 'float')
        category = self.try_catch_get('category', None, 'str')

        if latitude and longitude:
            threshold_latitude = distance / 110.574
            threshold_longitude = distance / (111.320 * math.cos(latitude / math.pi / 180))
            latitude_p = latitude + threshold_latitude
            latitude_m = latitude - threshold_latitude
            longitude_p = longitude + threshold_longitude
            longitude_m = longitude - threshold_longitude
            distance_Q = Q(company__latitude__range=[latitude_m, latitude_p], company__longitude__range=[longitude_m, longitude_p])
            parent = parent.filter(distance_Q)
        if category:
            parent = parent.filter(company__category__name__iexact=category)
        content_type = ['product']
        return parent.filter(expiry_date__gt=datetime.now().date(),
                                company__affilated_companies__isnull=True
                            )


class ProductCategoryBaseFilter(filters.FilterSet):
    company = filters.CharFilter(field_name='company__id')
    parent = filters.CharFilter(field_name='parent__id')
    name = filters.CharFilter(field_name='name__istartswith')
    types = filters.CharFilter(field_name='types')
    class Meta:
        model = ProductCategory
        fields = ['name', 'company', 'parent', 'types']


class ProductCategoryFilter(ProductCategoryBaseFilter):
    @property
    def qs(self):
        parent = super(ProductCategoryFilter, self).qs
        filter_by = self.request.GET.get('filter_by',None)
        company = getattr(self.request, 'company', None)
        if company:
            parent = parent.filter(company=company)
        if filter_by == 'has_child':
            parent = parent.filter(parent__isnull=True).order_by('position')
        return parent
