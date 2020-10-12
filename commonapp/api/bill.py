from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.serializers.bill import BillSerializer
from commonapp.models.bill import Bill
from permission import isCompanyOwnerAndAllowAll,isCompanyManagerAndAllowAll

class BillListView(generics.GenericAPIView):
    # permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BillSerializer

    def get(self, request):
        """
        An endpoint for listing all the bills. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        bill_obj = Bill.objects.all()
        paginator = Paginator(bill_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = BillSerializer(page_obj, many=True,\
            context={'request':request})
        data = {
            'success': 1,
            'bill': serializer.data,
        }
        return Response(data, status=200)
    
    def post(self,request):
        """
        An endpoint for creating bill.
        """
        serializer = BillSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'bill': serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.error,
        }
        return Response(data, status=400)

class BillDetailView(generics.GenericAPIView):
    # permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BillSerializer

    def get(self, request, bill_id):
        """
        An endpoint for getting bill detail.
        """
        bill_obj = Bill.objects.filter(id=bill_id)
        if bill_obj:
            serializer = BillSerializer(bill_obj[0], context={'request':request})
            data = {
                'success': 1,
                'bill': serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Bill doesn't exist.",
            }
            return Response(data, status=404)


    def delete(self, request, bill_id):
        """
        An endpoint for deleting bill.
        """
        bill_obj = Bill.objects.filter(id=bill_id)
        if bill_obj:
            try:
                bill_obj[0].delete()
                data = {
                    'success': 1,
                    'bill': 'Bill deleted successfully.'
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Bill cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Bill doesn't exist."
            }
            return Response(data, status=404)