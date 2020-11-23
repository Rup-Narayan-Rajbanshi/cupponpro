from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from rest_framework.permissions import IsAuthenticated
from helpers.api_mixins import FAPIMixin
from commonapp.models.image import Image
from productapp.serializers.product_image import ImageSerializer
from productapp.filters import CompanyProductImageFilter
from permission import isCompanyOwnerAndAllowAll

class CompanyProductImageAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                    mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CompanyProductImageFilter
    pagination_class = FPagination
    permission_classes = (isCompanyOwnerAndAllowAll, )
