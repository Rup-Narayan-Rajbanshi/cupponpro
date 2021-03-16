from rest_framework import generics
from rest_framework.response import Response
from orderapp.models.bills import Bills
from orderapp.filters import SellItemFilter, ServiceChargeFilter, SellFilter, TableSalesFilter, CreditFilter
from commonapp.models.asset import Asset
from commonapp.models.company import CompanyUser
from orderapp.models.order import Orders
from helpers.paginations import FPagination
from orderapp.serializers.order import TableSalesSerializer
from helpers.constants import ORDER_STATUS
from rest_framework import mixins
from permission import isCompanyManagerAndAllowAll, CompanyUserPermission
from django.db.models import Count, Sum, F, FloatField, Value
import math
from collections import OrderedDict
from productapp.models.product import Product
from userapp.models.customer import Customer
from django.db.models.functions import Coalesce


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
        total = 0.0
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
                    sales[order.created_at.date()]['total_amount']=sales[order.created_at.date()]['total_amount'] + order.get_grand_total_report(order) if 'total_amount' in sales[order.created_at.date()] else order.get_grand_total_report(order)
                    total = total  + order.get_grand_total_report(order) 
        sorting_method = request.query_params.get('sort_by', 'desc')
        if sorting_method == 'desc':
            sales = OrderedDict(sorted(sales.items(), reverse=True))
        else:
            sales = OrderedDict(sorted(sales.items(), reverse=False))
        page_number = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('size', 10))
        low_range = (page_number-1) * page_size
        high_range = page_number * page_size
        data = list(sales.values())[low_range:high_range]
        data = {
            'total_pages': math.ceil(len(sales)/page_size),
            'total_records': len(sales),
            'next': page_number + 1 if page_number + 1 <=math.ceil(len(sales)/page_size) else None,
            'previous': page_number - 1 if page_number - 1 > 0 else None,
            'record_range': [low_range + 1, len(data)+low_range],
            'current_page': page_number,
            'records': data,
            'grand_total_amount': total
        }
        return Response(data, status=200)
                

    def get_total_order(self, order):
        count = 0
        for lines in order.lines.all():
            count = count + 1
        return count


class GetServiceChargeAPI(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-created_at')
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

        orders_company = self.get_queryset().filter(company=company)
        orders_types = self.filter_queryset(self.queryset)
        orders_all = orders_types.intersection(orders_company)
        
        page_number = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('size', 10))
        low_range = (page_number-1) * page_size
        high_range = page_number * page_size
        sorting_method = request.query_params.get('sort_by', 'desc')
        if sorting_method == 'desc':
            orders = orders_all.order_by('-created_at')[low_range:high_range]
        else:
            orders = orders_all.order_by('created_at')[low_range:high_range]

        sales = dict()
        total = 0.0
        for order in orders:
            if str(order.id) not in sales:
                sales[str(order.id)]= dict()
            sales[str(order.id)]['order_id'] = order.id
            sales[str(order.id)]['date'] = order.created_at.date()
            sales[str(order.id)]['service_charge'] = order.service_charge_amount
            total = float(total) + float(order.service_charge_amount)
        # total = bills_all.aggregate(Sum('service_charge'))
        sales_values = list(sales.values())

        data = {
            'total_pages': math.ceil(len(orders_all)/page_size),
            'total_records': len(orders_all),
            'next': page_number + 1 if page_number + 1 <=math.ceil(len(orders_all)/page_size) else None,
            'previous': page_number - 1 if page_number - 1 > 0 else None,
            'record_range': [low_range + 1, len(sales_values)+low_range],
            'current_page': page_number,
            'records': sales_values,
            'total_service_charge': total
        }
        return Response(data, status=200)


class GetSellItemReportAPI(generics.ListAPIView):
    queryset = Orders.objects.all().order_by('-created_at')
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

        orders_company = self.get_queryset().filter(company=company)
        orders_types = self.filter_queryset(self.queryset)
        orders = orders_types.intersection(orders_company).values('id')

        page_number = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('size', 10))
        low_range = (page_number-1) * page_size
        high_range = page_number * page_size

        sales = dict()
        total = 0.0
        #splitting of bill by types:
        products_all = Product.objects.filter(order_lines__order__in=orders).distinct()
        products = products_all[low_range:high_range]
        for product in products:
            sales[product.name] = dict()
            sales[product.name]['name'] = product.name
            sales[product.name]['total_sold_quantity'] = product.order_lines.all().aggregate(Sum('quantity'))['quantity__sum']
            sales[product.name]['total_price'] = product.order_lines.all().aggregate(Sum('total'))['total__sum']
            total = float(total) + float(sales[product.name]['total_price'])

        # for order in orders:
        #     orderline = order.lines.all()
        #     if orderline:
        #         for line in orderline:
        #             product = line.product
        #             if product.name not in sales.keys():
        #                 sales[product.name] = dict()
        #             #sales['Grand_total'] = sales['Grand_total'] + line.total if 'Grand_total' in sales.keys() else line.total
        #             sales[product.name]['name'] = product.name
        #             sales[product.name]['total_sold_quantity'] = sales[product.name]['total_sold_quantity'] + line.quantity if 'total_sold_quantity' in sales[product.name].keys() else line.quantity
        #             sales[product.name]['total_price'] = sales[product.name]['total_price'] + line.total if 'total_price' in sales[product.name].keys() else line.total
        #             total = total + float(line.total)
        data = list(sales.values())
        data = {
            'total_pages': math.ceil(len(products_all)/page_size),
            'total_records': len(products_all),
            'next': page_number + 1 if page_number + 1 <=math.ceil(len(products_all)/page_size) else None,
            'previous': page_number - 1 if page_number - 1 > 0 else None,
            'record_range': [low_range + 1, len(data)+low_range],
            'current_page': page_number,
            'records': data,
            'grand_total_price': total
        }
        return Response(data, status=200)


class CreditReportAPI(generics.ListAPIView):
    queryset = Bills.objects.all().order_by('-created_at')
    filter_class = CreditFilter
    
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
        bills_all = bills_types.intersection(bills_company)
        customer_list = bills_all.order_by('customer').values_list('customer').distinct()
        print(customer_list)

        page_number = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('size', 10))
        low_range = (page_number-1) * page_size
        high_range = page_number * page_size
        
        customer_required = customer_list[low_range:high_range]
        customers_all = Customer.objects.filter(id__in=customer_list).distinct()
        customers = Customer.objects.filter(id__in=customer_required).distinct()

        sales = dict()
        total = 0.0

        for customer in customers:
            sales[customer.id] = dict()
            sales[customer.id]['name'] = customer.name
            sales[customer.id]['credit_amount'] = customer.bills.all().aggregate(Sum('credit_amount'))['credit_amount__sum']
            sales[customer.id]['paid_amount'] = customer.bills.all().aggregate(Sum('paid_amount'))['paid_amount__sum']
            sales[customer.id]['total_amount'] = customer.bills.all().aggregate(Sum('payable_amount'))['payable_amount__sum']
            total = total + float(sales[customer.id]['credit_amount'])

        data = list(sales.values())
        data = {
            'total_pages': math.ceil(len(customers_all)/page_size),
            'total_records': len(customers_all),
            'next': page_number + 1 if page_number + 1 <=math.ceil(len(customers_all)/page_size) else None,
            'previous': page_number - 1 if page_number - 1 > 0 else None,
            'record_range': [low_range + 1, len(data)+low_range],
            'current_page': page_number,
            'records': data,
            'total_credit': total
        }
        return Response(data, status=200)

    def get_paid_amount(self, bill):
        total = float(bill.payable_amount) - float(bill.credit_amount)
        return total

class TableSalesAPI(generics.ListAPIView):
    queryset = Asset.objects.all().order_by('-created_at')
    permission_classes = [CompanyUserPermission | isCompanyManagerAndAllowAll]
    filter_class = TableSalesFilter
    serializer_class = TableSalesSerializer
    pagination_class = FPagination

    def get_queryset(self):
        try:
            company = self.request.user.company_user.all().values_list('company', flat=True)[0] 
        except:
            company = None

        if not company:
            data = {
                'success': 0,
                'message': 'User is not part of any company'
            }
            return Response(data, status=403)
        queryset = Asset.objects.filter(company=company).annotate(number_of_sales=Count('orders__bill'), total_amount=Coalesce(Sum(F('orders__bill__payable_amount'),output_field=FloatField()),Value(0)))
        queryset = queryset.filter(number_of_sales__gt = 0.0)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            grand_total=queryset.aggregate(grand_total_amount=Coalesce(Sum(F('orders__bill__payable_amount'), output_field=FloatField()), Value(0)))['grand_total_amount']
            response = self.get_paginated_response(serializer.data)
            response.data.update({'grand_total_amount':grand_total})
            return response
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

   



   