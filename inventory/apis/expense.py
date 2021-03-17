from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from helpers.paginations import FPagination
from helpers.api_mixins import FAPIMixin
from rest_framework.response import Response
from permission import CompanyUserPermission
from inventory.models.expense import Expense, Payment
from inventory.serializers.expense import ExpenseSerializer, PaymentSerializer


class ExpenseAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Expense.objects.select_related('company').all().order_by('-created_at')
    serializer_class = ExpenseSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = FPagination
    permission_class = (CompanyUserPermission, )


    def get_queryset(self):
        try:
            company_user = self.request.user.company_user.all()
            company = company_user[0].company
        except:
            company=None
        queryset = Expense.objects.filter(company=company).order_by('-created_at')
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
                'message': 'Expense deleted Successfully'
            }
        except:
            data = {
                'success': 0,
                'message': 'Expense cannot be deleted.'
            }
        return Response(data, status=status)






class PaymentAPI(FAPIMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Payment.objects.select_related('company').all().order_by('-created_at')
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = FPagination
    permission_class = (CompanyUserPermission, )


    def get_queryset(self):
        try:
            company_user = self.request.user.company_user.all()
            company = company_user[0].company
        except:
            company=None
        queryset = Payment.objects.filter(company=company).order_by('-created_at')
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
                'message': 'Payment deleted Successfully'
            }
        except:
            data = {
                'success': 0,
                'message': 'Payment cannot be deleted.'
            }
        return Response(data, status=status)