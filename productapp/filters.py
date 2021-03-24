import math
from datetime import datetime
from django_filters import rest_framework as filters
from django.db.models import Q, Max
from commonapp.models.image import Image
from company.models.company import CompanyUser
from productapp.models.product import Product, ProductCategory
from productapp.models.coupon import Coupon
from django.db.models import Count
from django.utils import timezone


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
                                company__is_affiliate=True
                            )


class TrendingCouponFilter(CouponBaseFilter):
    @property
    def qs(self):
        parent = super(TrendingCouponFilter, self).qs
        content_type = ['productcategory']
        return parent.filter(expiry_date__gt=datetime.now().date(),
                                content_type__model__in=content_type,
                                company__is_affiliate=True
                            )


class RecentCouponFilter(CouponBaseFilter):
    @property
    def qs(self):
        parent = super(RecentCouponFilter, self).qs
        content_type = ['product']
        return parent.filter(expiry_date__gt=datetime.now().date(),
                                content_type__model__in=content_type,
                                company__is_affiliate=False
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
                                company__is_affiliate=False
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


class MenuBaseFilter(filters.FilterSet):
    company = filters.CharFilter(field_name='company__id')
    parent = filters.CharFilter(field_name='parent__id')
    name = filters.CharFilter(field_name='name__istartswith')
    types = filters.CharFilter(field_name='types')
    class Meta:
        model = ProductCategory
        fields = ['name', 'company', 'parent', 'types']


class MenuFilter(MenuBaseFilter):
    @property
    def qs(self):
        parent = super(MenuFilter, self).qs
        company = getattr(self.request, 'company', None)
        if company:
            parent = parent.filter(company=company, parent__isnull=True).order_by('position')
        return parent


class ProductFilter(filters.FilterSet):
    company = filters.CharFilter(field_name='company__id')

    class Meta:
        model = Product
        fields = ['company',]

class SpecialFoodFilter(ProductFilter):
    @property
    def qs(self):
        parent = super(SpecialFoodFilter, self).qs
        special_product = parent.annotate(special_food_count=Count('order_lines')).\
                            order_by('-special_food_count')[:5]

        return special_product


class CouponFilter(filters.FilterSet):
    company = filters.CharFilter(field_name='company__id')
    class Meta:
        model = Coupon
        fields = "__all__"


class HighestDiscountCouponFilter(CouponFilter):
    @property
    def qs(self):
        parent = super(HighestDiscountCouponFilter, self).qs
        status = self.request.GET.get('status',None)
        if status == 'max_discount':
            coupon = parent.filter(discount_type='PERCENTAGE',
                                expiry_date__gte=timezone.now()
                                ).annotate(highest_discount=Max('discount')).order_by('-highest_discount')[:1]
            if coupon:
                return coupon
            else:
                return parent.filter(discount_type='FLAT',
                                expiry_date__gte=timezone.now()
                                ).annotate(highest_discount=Max('discount')).order_by('-highest_discount')[:1]

        return parent.filter(expiry_date__gte=timezone.now())


class GlobalCouponFilter(filters.FilterSet):
    company = filters.CharFilter(field_name='company__id')
    name = filters.CharFilter(field_name='name',lookup_expr='icontains')
    discount_type = filters.CharFilter(field_name='discount_type',lookup_expr='icontains')
    discount = filters.RangeFilter(field_name='discount')
   
    class Meta:
        model = Coupon
        fields = "__all__"

    @property
    def qs(self):
        parent = super(GlobalCouponFilter, self).qs
        q = self.request.GET.get('q',None)
        category = self.request.GET.get('category',None)

        order_by_fields = ['created_at', 'low_to_high', 'high_to_low']
        order_by = self.request.GET.get('order_by') if self.request.GET.get('order_by') in order_by_fields else 'id'
        if order_by == 'low_to_high':
           order_by='discount'
        elif order_by == 'high_to_low':
            order_by='-discount'

        if q:
            product_obj_ids= Product.objects.filter(tag__icontains=q).values_list('id',flat=True)
            
            product_category_obj_ids= ProductCategory.objects.filter(tag__icontains=q).values_list('id',flat=True)

            parent = parent.filter(Q(company__name__icontains=q)|
                                    Q(object_id__in=product_obj_ids)|
                                    Q(object_id__in=product_category_obj_ids)
                                    )
        elif q == '':
            raise ValidationError({'detail': 'No search input given'})
         
        if category:
            parent = parent.filter(object_id=category)

        coupons = parent
        coupons = coupons.filter(expiry_date__gte=timezone.now()).order_by('{order_by}'.format(order_by=order_by))

        return coupons


