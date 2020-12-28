import math
from django.db.models import Q
from django_filters import rest_framework as filters
from userapp.models import User
from commonapp.models.company import FavouriteCompany, CompanyUser, Company
from company.models import Partner


class FavouriteCompanyBaseFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user__id')
    company = filters.CharFilter(field_name='company__id')

    class Meta:
        model = FavouriteCompany
        fields = ['user', 'company', 'is_favourite']


class FavouriteCompanyUserFilter(FavouriteCompanyBaseFilter):
    @property
    def qs(self):
        parent = super(FavouriteCompanyUserFilter, self).qs
        company_user = CompanyUser.objects.filter(user=self.request.user).first()
        if company_user:
            return parent.filter(company=company_user.company)
        return parent.none()


class UserFavouriteCompanyFilter(FavouriteCompanyBaseFilter):
    @property
    def qs(self):
        parent = super(UserFavouriteCompanyFilter, self).qs
        return parent.filter(user=self.request.user)


class CompanyBaseFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='user__id')

    class Meta:
        model = Company
        fields = ['author', 'name']


class LocalBusinessFilter(CompanyBaseFilter):

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
        parent = super(LocalBusinessFilter, self).qs
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
            distance_Q = Q(latitude__range=[latitude_m, latitude_p], longitude__range=[longitude_m, longitude_p])
            parent = parent.filter(distance_Q)
        if category:
            parent = parent.filter(category__name__iexact=category)
        return parent.filter(affilated_companies__isnull=True,
                            # company_coupons__isnull=False
                        ).distinct()


class PartnerBaseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name__istartswith')

    class Meta:
        model = Partner
        fields = ['name']
