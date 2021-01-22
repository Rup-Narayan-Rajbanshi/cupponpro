from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from rest_framework.permissions import AllowAny
from helpers.api_mixins import FAPIMixin
from company.models import Partner
from company.serializers.partner import PartnerSerializer
from company.filters import PartnerBaseFilter
from permission import isCompanyOwnerAndAllowAll

class PartnerAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Partner.objects.all().order_by('name')
    serializer_class = PartnerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PartnerBaseFilter
    pagination_class = FPagination
    permission_classes = (AllowAny, )
