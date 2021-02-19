from rest_framework import generics
from rest_framework.response import Response
from orderapp.models.bills import Bills
from orderapp.filters import SellItemFilter, ServiceChargeFilter, SellFilter, TableSalesFilter
from commonapp.models.asset import Asset
from commonapp.models.company import CompanyUser
from orderapp.models.order import Orders
from helpers.paginations import FPagination
from orderapp.serializers.order import TableSalesSerializer
from helpers.constants import ORDER_STATUS
from rest_framework import mixins
from permission import isCompanyManagerAndAllowAll, CompanyUserPermission
from django.db.models import Count, Sum


class GetSellReport(generics.ListAPIView):
    queryset = Bills.objects.all().order_by('-created_at')
    filter_class = SellFilter

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
                    if order.created_at.date() not in sales:
                        sales[order.created_at.date()]= dict()
                    sales[order.created_at.date()]['date'] = str(order.created_at.date())
                    if 'invoice_number' not in sales[order.created_at.date()]:
                        sales[order.created_at.date()]['invoice_number'] = [bill.invoice_number]
                    else:
                        if bill.invoice_number not in sales[order.created_at.date()]['invoice_number']:
                            sales[order.created_at.date()]['invoice_number'].append(bill.invoice_number) 
                    if 'customer_name' not in sales[order.created_at.date()]:
                        sales[order.created_at.date()]['customer_name'] = list()
                        if bill.customer:
                            sales[order.created_at.date()]['customer_name'].append(bill.customer.name)
                    else:
                        if bill.customer:
                            if bill.customer.name not in sales[order.created_at.date()]['customer_name']:
                                sales[order.created_at.date()]['customer_name'].append(bill.customer.name)
                    if 'payment_method' not in sales[order.created_at.date()]:
                        sales[order.created_at.date()]['payment_method'] = [bill.payment_mode]
                    else:
                        if bill.payment_mode not in sales[order.created_at.date()]['payment_method']:
                            sales[order.created_at.date()]['payment_method'].append(bill.payment_mode)
                    # sales[order.created_at.date()]['payment_method']=bill.payment_mode
                    sales[order.created_at.date()]['order_total']= sales[order.created_at.date()]['order_total'] + self.get_total_order(order) if 'order_total' in sales[order.created_at.date()] else self.get_total_order(order)
                    sales[order.created_at.date()]['tax']=bill.company.tax if bill.company.tax else 0
                    sales[order.created_at.date()]['service_charge']=sales[order.created_at.date()]['service_charge'] + order.service_charge_amount if 'service_charge' in sales[order.created_at.date()] else order.service_charge_amount
                    sales[order.created_at.date()]['discount']=sales[order.created_at.date()]['discount'] + order.discount_amount if 'discount' in sales[order.created_at.date()] else order.discount_amount
                    sales[order.created_at.date()]['total_amount']=sales[order.created_at.date()]['total_amount'] + order.get_grand_total(order) if 'total_amount' in sales[order.created_at.date()] else order.get_grand_total(order)

        data = {
            'total_records': len(sales),
            'data': sales.values()
        }
        return Response(data, status=200)
                

    def get_total_order(self, order):
        count = 0
        for lines in order.lines.all():
            count = count + 1
        return count


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


class CreditReportAPI(generics.ListAPIView):
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
            if bill.customer:
                if bill.customer.name not in sales:
                    sales[bill.customer.name] = dict()
                sales[bill.customer.name]['name'] = bill.customer.name
                sales[bill.customer.name]['credit_amount'] = sales[bill.customer.name]['credit_amount'] + bill.credit_amount if 'credit_amount' in sales[bill.customer.name] else bill.credit_amount
                sales[bill.customer.name]['paid_amount'] = sales[bill.customer.name]['paid_amount'] + self.get_paid_amount(bill) if 'paid_amount' in sales[bill.customer.name] else self.get_paid_amount(bill)
        data = {
            'total_records': len(sales),
            'data': sales.values()
        }
        return Response(data, status=200)

    def get_paid_amount(self, bill):
        total = float(bill.payable_amount) - float(bill.credit_amount)
        return total

class TableSalesAPI(generics.ListAPIView):
    queryset = Asset.objects.filter().order_by('-created_at')
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    serializer_class = TableSalesSerializer
    pagination_class = FPagination
    filter_class = TableSalesFilter

    def get_queryset(self):
        company_user = CompanyUser.objects.filter(user=self.request.user)[0]
        asset = Asset.objects.filter(company=company_user.company).annotate(number_of_sales=Count('orders__bill'), order_total=Sum('orders__bill__payable_amount'))
        
        return asset


   