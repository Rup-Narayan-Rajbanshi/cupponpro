from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from inventory.models.stock import Stock
from inventory.serializers.stock import StockSerializer
from rest_framework.response import Response
from permission import CompanyUserPermission



class StockAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Stock.objects.select_related('company').all().order_by('-created_at')
    serializer_class = StockSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = FPagination
    permission_class = (CompanyUserPermission, )


    def get_queryset(self):
        try:
            company_user = self.request.user.company_user.all()
            company = company_user[0].company
        except:
            company=None
        queryset = Stock.objects.filter(company=company).order_by('-created_at')
        return queryset


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = dict()
        status = 403
        try:
            instance.delete()
            status = 200
            data = {
                'success': 1,
                'message': 'Inventory deleted Successfully'
            }
        except:
            data = {
                'success': 0,
                'message': 'Inventory cannot be deleted.'
            }
        return Response(data, status=status)




