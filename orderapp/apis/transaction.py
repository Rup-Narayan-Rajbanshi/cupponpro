from orderapp.serializers.transaction import TransactionHistoryBillSerializer
from orderapp.models.transaction import TransactionHistoryBills
from helpers.api_mixins import FAPIMixin
from rest_framework.viewsets import GenericViewSet
from helpers.paginations import FPagination
from permission import CompanyUserPermission
from rest_framework import mixins
from orderapp.filters import TransactionFilter
from rest_framework import generics
from orderapp.serializers.bill import BillCreateSerializer
from orderapp.models.bills import Bills
from rest_framework.response import Response

class BillTransactionHistoryAPI(FAPIMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = TransactionHistoryBills.objects.all().order_by('-created_at')
    serializer_class = TransactionHistoryBillSerializer
    pagination_class = FPagination
    permission_classes = (CompanyUserPermission, )
    filter_class = TransactionFilter

    def get_queryset(self):
        company = getattr(self.request, 'company', None)
        queryset = TransactionHistoryBills.objects.filter(bill__company=company).order_by('-created_at')
        return queryset


class CustomerCreditPaymentAPI(generics.CreateAPIView):
    queryset = Bills.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        customer  = request.data['customer']
        paid_amount = float(request.data['paid_amount'])
        bills = Bills.objects.filter(customer=customer, is_credit=True).order_by('created_at')
        for bill in bills:
            credit_amount = float(bill.credit_amount)
            temp_paid = paid_amount
            paid_amount = paid_amount - credit_amount
            if paid_amount <= 0:
                data = {'paid_amount': temp_paid}
                serializer = BillCreateSerializer(instance=bill, data=data, context={'request':request}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message':'Updated bill payment (not all credit paid)'}, status=200)
            else:
                data = {'paid_amount': credit_amount}
                serializer = BillCreateSerializer(instance=bill, data=data, context={'request':request}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return Response({'message':'Updated bill payment'}, status=200)
