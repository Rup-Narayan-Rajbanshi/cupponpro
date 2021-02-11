from rest_framework import generics
from rest_framework.response import Response
from orderapp.models.bills import Bills
from orderapp.filters import SalesFilter

class GetSalesReportAPI(generics.ListAPIView):
    queryset = Bills.objects.all()
    filter_class = SalesFilter
    
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
            order = bill.orders.all()
            if order:
                orderline = order[0].lines.all()
                for line in orderline:
                    product = line.product
                    if product.name not in sales.keys():
                        sales[product.name] = dict()
                    sales['Grand_total'] = sales['Grand_total'] + line.total if 'Grand_total' in sales.keys() else line.total
                    sales[product.name]['Total sold quantity'] = sales[product.name]['Total sold quantity'] + line.quantity if 'Total sold quantity' in sales[product.name].keys() else line.quantity
                    sales[product.name]['Selling price'] = product.selling_currency + str(product.total_price)
                    sales[product.name]['Total price'] = sales[product.name]['Total price'] + line.total if 'Total price' in sales[product.name].keys() else line.total
        data = {
            'sales': sales
            #'bar': sales_bar
        }
        return Response(data, status=200)


        
