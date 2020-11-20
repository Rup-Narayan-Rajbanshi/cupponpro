from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from rest_framework.permissions import IsAuthenticated
from helpers.api_mixins import FAPIMixin
from commonapp.models.company import FavouriteCompany
from company.serializers.company import FavouriteCompanySerializer
from company.filters import FavouriteCompanyUserFilter, UserFavouriteCompanyFilter
from permission import isCompanyOwnerAndAllowAll

class FavouriteCompanyUserAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = FavouriteCompany.objects.select_related('company', 'user').all()
    serializer_class = FavouriteCompanySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = FavouriteCompanyUserFilter
    pagination_class = FPagination
    permission_classes = (isCompanyOwnerAndAllowAll, )


class UserFavouriteCompanyAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = FavouriteCompany.objects.select_related('company', 'user').all()
    serializer_class = FavouriteCompanySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFavouriteCompanyFilter
    pagination_class = FPagination
    permission_classes = (IsAuthenticated, )
