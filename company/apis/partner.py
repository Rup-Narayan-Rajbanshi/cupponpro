from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from rest_framework.permissions import AllowAny
from helpers.api_mixins import FAPIMixin
from rest_framework.response import Response
from company.models.partner import Partner, DeliveryPartner
from company.serializers.partner import PartnerSerializer, DeliveryPartnerSerializer
from company.filters import PartnerBaseFilter
from permission import CompanyUserPermission

class PartnerAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Partner.objects.all().order_by('name')
    serializer_class = PartnerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PartnerBaseFilter
    pagination_class = FPagination
    permission_classes = (AllowAny, )




class DeliveryPartnerAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = DeliveryPartner.objects.all().order_by('name')
    serializer_class = DeliveryPartnerSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = FPagination
    permission_classes = (CompanyUserPermission, )

    def get_queryset(self):
        company = getattr(self.request, 'company', None)
        queryset = DeliveryPartner.objects.filter(company=company)
        return queryset


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        status = 200
        if instance:
            instance.delete()
            data={
                'success': 1,
                'message': 'Deleted one delivery partner'
            }
        else:
            data={
                'success': 0,
                'message': 'Delivery partner does not exit.'
            }
        return Response(data, status=status)

