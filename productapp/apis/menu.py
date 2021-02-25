from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from commonapp.models.product import ProductCategory
from productapp.serializers.menu import (
    MenuSerializer
)
from productapp.filters import (
    MenuFilter
)
from permission import CompanyUserPermission, isAdmin, isCompanySalePersonAndAllowAll, publicReadOnly


class MenuAPI(FAPIMixin,  mixins.ListModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.select_related('company', 'parent').all().order_by('position')
    serializer_class = MenuSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MenuFilter
    # pagination_class = FPagination
    permission_classes = ((CompanyUserPermission | isAdmin | isCompanySalePersonAndAllowAll | publicReadOnly ),)

