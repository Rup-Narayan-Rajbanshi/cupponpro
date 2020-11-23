from django_filters import rest_framework as filters
from commonapp.models.image import Image
from commonapp.models.company import CompanyUser
from commonapp.models.product import Product


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
