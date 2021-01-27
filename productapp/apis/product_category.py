from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from helpers.constants import COUPON_TYPE_DISPLAY_MAPPER
from commonapp.models.product import ProductCategory
from productapp.serializers.product_category import (
    ProductCategorySerializer
)
from productapp.filters import (
    ProductCategoryFilter
)
from permission import CompanyUserPermission, isAdmin


class ProductCategoryAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.select_related('company').all().order_by('name')
    serializer_class = ProductCategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductCategoryFilter
    pagination_class = FPagination
    permission_classes = (IsAuthenticated, (isAdmin | CompanyUserPermission))
