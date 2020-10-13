from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.serializers.salesitem import SalesItemSerializer
from commonapp.models.salesitem import SalesItem
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll

class SalesItemListView(generics.GenericAPIView):
    # permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = SalesItemSerializer

    def get(self, request, bill_id):
        """
        An endpoint for listing all the salesitem of the bill.
        """
        sales_item_obj = SalesItem.objects.filter(bill__id=bill_id)
        if sales_item_obj:
            serializer = SalesItemSerializer(sales_item_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'Sales item not found.',
            }
            return Response(data, status=400)
    
    def post(self, request, bill_id):
        """
        An endpoint for creating salesitem of the bill.
        """
        if int(request.data['bill']) == bill_id:
            serializer = SalesItemSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data,
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

class SalesItemDetailView(generics.GenericAPIView):
    # permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = SalesItemSerializer

    def get(self, request, item_id):
        """
        An endpoint for getting salesitem detail.
        """
        item_obj = SalesItem.objects.filter(id=item_id)
        if item_obj:
            serializer = SalesItemSerializer(item_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Sales Item doesn't exist."
            }
            return Response(data, status=404)
    
    def delete(self, request, item_id):
        """
        An endpoint for deleting salesitem.
        """
        item_obj = SalesItem.objects.filter(id=item_id)
        if item_obj:
            try:
                item_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Sales Item cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Sales Item doesn't exist."
            }
            return Response(data, status=404)
