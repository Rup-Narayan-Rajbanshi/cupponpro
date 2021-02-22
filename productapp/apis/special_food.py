from rest_framework.viewsets import GenericViewSet, mixins
from commonapp.serializers.product import ProductSerializer
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from productapp.filters import SpecialFoodFilter
from commonapp.models.product import Product

class SpecialFoodAPI(FAPIMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.select_related('company').all()
    serializer_class = ProductSerializer
    pagination_class = FPagination
    filter_class = SpecialFoodFilter
