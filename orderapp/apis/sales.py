from rest_framework import generics
from rest_framework.response import Response
from orderapp.models.bills import Bills
from orderapp.filters import SellItemFilter, ServiceChargeFilter #SellFilter
from commonapp.models.asset import Asset
from commonapp.models.company import CompanyUser
from orderapp.models.order import Orders
from helpers.paginations import FPagination
from orderapp.serializers.order import TableSalesSerializer
from helpers.constants import ORDER_STATUS
from rest_framework import mixins
from permission import isCompanyManagerAndAllowAll, CompanyUserPermission
from django.db.models import Count


class GetSellReport(generics.ListAPIView):
    queryset = Bills.objects.all().order_by('-created_at')
    #filter_class = SellFilter

    def list(self, request):
        try:
            company = request.user.company_user.all().values_list('company', flat=True)[0] 
        except:
            company = None

        if not company:
            data = {
                'success': 0,
                'message': 'User is not part of any company'
            }
            return Response(data, status=403)

        bills_company = self.get_queryset().filter(company=company)
        bills_types = self.filter_queryset(self.queryset)
        bills = bills_types.intersection(bills_company)

        sales = dict()
        for bill in bills:
            orders = bill.orders.all()
            if orders:
                for order in orders:
                    if order.created_at not in sales:
                        sales[order.created_at]= dict()
                    if 'invoice_number' not in sales[order.created_at]:
                        sales[order.created_at]['invoice_number'] = [bill.invoice_number]
                    else:
                        sales[order.created_at]['invoice_number'].append(bill.invoice_number) 
                    if 'customer_name' not in sales[order.created_at]:
                        sales[order.created_at]['customer_name'] = list()
                        sales[order.created_at]['customer_name'].append(bill.customer.name) if bill.customer
                    else:
                        sales[order.created_at]['customer_name'].append(bill.customer.name) if bill.customer
                    sales[order.created_at]['payment_method']=bill.payment_mode
                    sales[order.created_at]['order_total']=Count(order.lines.all())
                    sales[order.created_at]['tax']=bill.company.tax if bill.company.tax else 0
                    sales[order.created_at]['service_charge']=order.service_charge
                    sales[order.created_at]['discount']=order.discount_amount()
                    sales[order.created_at]['total_amount']=bill.get_grand_total()
                



class GetServiceChargeAPI(generics.ListAPIView):
    queryset = Bills.objects.all().order_by('-created_at')
    filter_class = ServiceChargeFilter

    def list(self, request):
        try:
            company = request.user.company_user.all().values_list('company', flat=True)[0] 
        except:
            company = None

        if not company:
            data = {
                'success': 0,
                'message': 'User is not part of any company'
            }
            return Response(data, status=403)

        bills_company = self.get_queryset().filter(company=company)
        bills_types = self.filter_queryset(self.queryset)
        bills = bills_types.intersection(bills_company)

        sales = dict()
        for bill in bills:
            orders = bill.orders.all()
            if orders:
                for order in orders:
                    if str(order.id) not in sales:
                        sales[str(order.id)]= dict()
                    sales[str(order.id)]['id'] = order.id
                    sales[str(order.id)]['service_charge'] = order.service_charge_amount
        data = {
            'total_records': len(sales),
            'data': sales.values()
        }
        return Response(data, status=200)


class GetSellItemReportAPI(generics.ListAPIView):
    queryset = Bills.objects.all().order_by('-created_at')
    filter_class = SellItemFilter
    
    def list(self, request):

        try:
            company = request.user.company_user.all().values_list('company', flat=True)[0] 
        except:
            company = None

        if not company:
            data = {
                'success': 0,
                'message': 'User is not part of any company'
            }
            return Response(data, status=403)

        bills_company = self.get_queryset().filter(company=company)
        bills_types = self.filter_queryset(self.queryset)
        bills = bills_types.intersection(bills_company)

        sales = dict()
        #splitting of bill by types:
        for bill in bills:
            orders = bill.orders.all()
            if orders:
                for order in orders:
                    orderline = order.lines.all()
                    if orderline:
                        for line in orderline:
                            product = line.product
                            if product.name not in sales.keys():
                                sales[product.name] = dict()
                            #sales['Grand_total'] = sales['Grand_total'] + line.total if 'Grand_total' in sales.keys() else line.total
                            sales[product.name]['name'] = product.name
                            sales[product.name]['Total sold quantity'] = sales[product.name]['Total sold quantity'] + line.quantity if 'Total sold quantity' in sales[product.name].keys() else line.quantity
                            sales[product.name]['Total price'] = sales[product.name]['Total price'] + line.total if 'Total price' in sales[product.name].keys() else line.total
        data = {
            'total_records': len(sales),
            'data': sales.values()
            #'bar': sales_bar
        }
        return Response(data, status=200)



class TableSalesAPI(generics.ListAPIView):
    queryset = Asset.objects.filter().order_by('-created_at')
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    serializer_class = TableSalesSerializer
    pagination_class = FPagination

    def get_queryset(self):
        company_user = CompanyUser.objects.filter(user=self.request.user)[0]
        asset = Asset.objects.filter(company=company_user.company).annotate(number_of_sales=Count('orders__bill'))
        
        return asset


   