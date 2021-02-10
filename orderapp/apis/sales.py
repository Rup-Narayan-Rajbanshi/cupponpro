from rest_framework import generics
from rest_framework.response import Response
from orderapp.models.bills import Bills
from orderapp.serializers.bill import BillListSerializer

class GetSalesReportAPI(generics.GenericAPIView):
    
    def get(self, request):

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
        print(company)
        bills = Bills.objects.filter(company=company)
        sales = dict()
        sales_food = dict()
        sales_bar = dict()
        #splitting of bill by types:
        for bill in bills:
            order = bill.orders.all()
            if order:
                orderline = order[0].lines.all()
                for line in orderline:
                    product = line.product
                    if product.product_category.types == 'FOOD':
                        sales_food['count of'+product.name] = sales_food['count of'+product.name] + 1 if 'count of'+product.name in sales_food.keys() else 1
                        sales_food['price of ' + product.name] = product.selling_currency + str(product.selling_price)
                        sales_food['Grand_total'] = sales_food['Grand_total'] + lines.total if 'Grand Total' in sales_food.keys() else line.total
                    elif product.product_category.types == 'BAR':
                        sales_bar['count of'+product.name] = sales_bar['count of'+product.name] + 1 if 'count of'+product.name in sales_bar.keys() else 1
                        sales_bar['price of ' + product.name] = product.selling_currency + str(product.selling_price)
                        sales_bar['Grand_total'] = sales_bar['Grand_total'] + lines.total if 'Grand_total' in sales_bar.keys() else line.total
        data = {
            'food': sales_food,
            'bar': sales_bar
        }
        return Response(data, status=200)


        
