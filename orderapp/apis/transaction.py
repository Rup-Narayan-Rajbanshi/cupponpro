from orderapp.serializers.transaction import TransactionHistoryBillSerializer
from orderapp.models.transaction import TransactionHistoryBills
from helpers.api_mixins import FAPIMixin
from rest_framework.viewsets import GenericViewSet
from helpers.paginations import FPagination
from permission import CompanyUserPermission
from rest_framework import mixins

class BillTransactionHistoryAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = TransactionHistoryBills.objects.all().order_by('-created_at')
    serializer_class = TransactionHistoryBillSerializer
    pagination_class = FPagination
    permission_classes = (CompanyUserPermission, )

    def get_queryset(self):
        company = getattr(self.request, 'company', None)
        queryset = TransactionHistoryBills.objects.filter(bill__company=company).order_by('-created_at')
        return queryset