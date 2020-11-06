from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from commonapp.models.order import OrderLine
from commonapp.serializers.order import OrderLineSerializer
from helper import isCompanyUser
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, isCompanySalePersonAndAllowAll, publicReadOnly

class OrderListView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = OrderLineSerializer

    def get(self, request, company_id, asset_id):
        """
        An endpoint for listing all the vendor's active order. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        order_obj = OrderLine.objects.filter(company=company_id, asset=asset_id, is_billed=False)
        paginator = Paginator(order_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = OrderLineSerializer(page_obj, many=True,\
            context={'request':request})
        if page_obj.has_previous():
            previous_page = page_obj.previous_page_number()
        else:
            previous_page = None
        if page_obj.has_next():
            next_page = page_obj.next_page_number()
        else:
            next_page = None
        data = {
            'success': 1,
            'previous_page': previous_page,
            'next_page': next_page,
            'page_count': paginator.num_pages,
            'data': serializer.data
        }
        return Response(data, status=200)
    
    def post(self, request, company_id, asset_id):
        """
        An endpoint for creating vendor's order.
        """
        serializer = OrderLineSerializer(data=request.data, many=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)

class OrderDetailView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = OrderLineSerializer

    def get(self, request, company_id, asset_id, order_id):
        """
        An endpoint for getting vendor's order detail.
        """
        order_obj = OrderLine.objects.filter(id=order_id, company=company_id, asset=asset_id)
        if order_obj:
            serializer = OrderLineSerializer(order_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Order doesn't exist.",
            }
            return Response(data, status=404)

    def put(self, request, company_id, asset_id, order_id):
        """
        An endpoint for updating vendor's order.
        """
        order_obj = OrderLine.objects.filter(id=order_id, company=company_id, asset=asset_id)
        if order_obj:
            serializer = OrderLineSerializer(instance=order_obj[0], data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 1,
                'message': "Order doesn't exist.",
            }
            return Response(data, status=404)

    def delete(self, request, company_id, asset_id, order_id):
        """
        An endpoint for deleting vendor's order.
        """
        order_obj = OrderLine.objects.filter(id=order_id, company=company_id, asset=asset_id)
        if order_obj:
            try:
                order_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Order cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Order doesn't exist."
            }
            return Response(data, status=404)

class ActiveOrderListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll]
    # serializer_class = 

    def get(self, request, company_id):
        """
        An endpoint for getting vendor's active order.
        """
        order_obj = OrderLine.objects.filter(company=company_id, is_billed=False)
        asset_names = []
        for order in order_obj:
            if order.asset.name not in asset_names:
                asset_names.append(order.asset.name)
        
        asset_wise_order_list = []
        for asset_name in asset_names:
            asset_wise_order = dict()
            asset_wise_order['asset'] = asset_name
            asset_wise_order_obj = order_obj.filter(asset__name=asset_name)
            serializer = OrderLineSerializer(asset_wise_order_obj, many=True, context={'request':request})
            asset_wise_order['order'] = serializer.data
            asset_wise_order_list.append(asset_wise_order)

        data = {
            'success': 1,
            'data': asset_wise_order_list
        }
        return Response(data, status=200)

class OrderToBillView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll]

    def get(self, request, company_id):
        """
        An endpoint for converting vendor's active order into billable sales item.
        """
        orders = request.data
        sales_item = []

        for order in orders:
            if order['state'] != 'Cancelled':
                order.pop('state')
                order.pop('asset')
                order['order'] = order.pop('id')
                order['discount'] = None
                order['total'] = order['rate'] * order['quantity']
                order['voucher'] = None
                sales_item.append(order)

        data = {
            'success': 1,
            'data': sales_item
        }
        return Response(data, status=200)
