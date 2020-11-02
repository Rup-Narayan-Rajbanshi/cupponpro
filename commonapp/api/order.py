from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from commonapp.models.order import Order
from commonapp.serializers.order import OrderSerializer
from helper import isCompanyUser
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, publicReadOnly

class OrderListView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = OrderSerializer

    def get(self, request, company_id, asset_id):
        """
        An endpoint for listing all the vendor's active order. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        order_obj = Order.objects.filter(company=company_id, asset=asset_id, is_delivered=False)
        paginator = Paginator(order_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = OrderSerializer(page_obj, many=True,\
            context={'request':request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)
    
    def post(self, request, company_id, asset_id):
        """
        An endpoint for creating vendor's order.
        """
        serializer = OrderSerializer(data=request.data, many=True, context={'request':request})
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
    serializer_class = OrderSerializer

    def get(self, request, company_id, asset_id, order_id):
        """
        An endpoint for getting vendor's order detail.
        """
        order_obj = Order.objects.filter(id=order_id, company=company_id, asset=asset_id)
        if order_obj:
            serializer = OrderSerializer(order_obj[0], context={'request':request})
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
        order_obj = Order.objects.filter(id=order_id, company=company_id, asset=asset_id)
        if order_obj:
            serializer = OrderSerializer(instance=order_obj[0], data=request.data, context={'request':request})
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
        order_obj = Order.objects.filter(id=order_id, company=company_id, asset=asset_id)
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
