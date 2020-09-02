from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from billapp.serializers.salesitem import SalesItemSerializer
from billapp.models.salesitem import SalesItem
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll

class SalesItemListView(APIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = SalesItemSerializer

    def get(self, request, bill_id):
        sales_item_obj = SalesItem.objects.filter(bill__id=bill_id)
        if sales_item_obj:
            serializer = SalesItemSerializer(sales_item_obj[0], context={'request':request})
            data = {
                'success': 1,
                'sales_item': serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'Sales item not found.',
            }
            return Response(data, status=400)
    
    def post(self, request, bill_id):
        if int(request.data['bill']) == bill_id:
            serializer = SalesItemSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'salesitem': serializer.data,
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors,
            }
            return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': 'Sales item cannot be created',
            }
            return Response(data, status=400)