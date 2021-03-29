from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination, FMaxPagination
from helpers.api_mixins import FAPIMixin
from helpers.constants import COUPON_TYPE_DISPLAY_MAPPER
from productapp.models.product import ProductCategory
from productapp.serializers.product_category import (
    ProductCategorySerializer
)
from productapp.filters import (
    ProductCategoryFilter
)
from permission import CompanyUserPermission, isAdmin, isCompanySalePersonAndAllowAll, publicReadOnly


class ProductCategoryAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ProductCategory.objects.select_related('company', 'parent').all().order_by('position')
    serializer_class = ProductCategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductCategoryFilter
    pagination_class = FMaxPagination
    permission_classes = ((CompanyUserPermission | isAdmin | isCompanySalePersonAndAllowAll | publicReadOnly ),)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = dict()
        status = 403
        try:
            instance.delete()
            status = 200
            data = {
                'success': 1,
                'message': 'Deleted Successfully'
            }
        except:
            data = {
                'success': 0,
                'message': 'This Product Category cannot be deleted because. This category is already processed in order'
            }
        return Response(data, status=status)
