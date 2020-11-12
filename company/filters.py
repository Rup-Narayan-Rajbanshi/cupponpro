from django_filters import rest_framework as filters
from userapp.models import User
from commonapp.models.company import FavouriteCompany, CompanyUser


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
        return None
