from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from inventory.models.purchase import Purchase, PurchaseTransaction
from inventory.serializers.purchase import PurchaseSerializer, PurchaseTransactionSerializer
from rest_framework.response import Response
from permission import CompanyUserPermission
from django.db.models import Sum, Count
from inventory.filters import PurchaseFilter







class PurchaseAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Purchase.objects.select_related('company').all().order_by('-created_at')
    serializer_class = PurchaseSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PurchaseFilter
    pagination_class = FPagination
    permission_class = (CompanyUserPermission, )

    def get_queryset(self):
        try:
            company_user = self.request.user.company_user.all()
            company = company_user[0].company
        except:
            company=None
        queryset = Purchase.objects.filter(stock__company=company).order_by('-created_at')
        # purchase = queryset.aggregate(total_items = Count('stock'), grand_total = Sum('total_amount'))
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
                'message': 'Purchase deleted Successfully'
            }
        except:
            data = {
                'success': 0,
                'message': 'Purchase cannot be deleted.'
            }
        return Response(data, status=status)






class PurchaseTransactionAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = PurchaseTransaction.objects.select_related('purchase').all().order_by('-created_at')
    serializer_class = PurchaseTransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = FPagination
    permission_class = (CompanyUserPermission, )

    def get_queryset(self):
        try:
            company_user = self.request.user.company_user.all()
            company = company_user[0].company
        except:
            company=None
        queryset = PurchaseTransaction.objects.filter(purchase__stock__company=company).order_by('-created_at')
        return queryset