from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.product import Product
from commonapp.models.bill import Bill
from commonapp.serializers.bill import BillSerializer, BillSaveSerializer
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, isCompanySalePersonAndAllowAll

class BillListView(generics.GenericAPIView):
    # permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BillSerializer

    def get(self, request, company_id):
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
            'data': serializer.data
        }
        return Response(data, status=200)
    
    def post(self,request, company_id):
        """
        An endpoint for creating bill.
        """
        serializer = BillSaveSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            temp_data = dict(serializer.data)
            sales_item = temp_data.pop('sales')
            temp_data['sales_item'] = sales_item
            data = {
                'success': 1,
                'data': temp_data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)

class BillDetailView(generics.GenericAPIView):
    # permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BillSerializer

    def get(self, request, company_id, bill_id):
        """
        An endpoint for getting bill detail.
        """
        bill_obj = Bill.objects.filter(id=bill_id, company=company_id)
        if bill_obj:
            serializer = BillSerializer(bill_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Bill doesn't exist.",
            }
            return Response(data, status=404)

    def put(self,request, company_id, bill_id):
        """
        An endpoint for updating bill.
        """
        bill_obj = Bill.objects.filter(id=bill_id, company=company_id)
        if bill_obj:
            serializer = BillSerializer(instance=bill_obj[0], data=request.data, context={'request':request})
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
        else:
            data = {
                'success': 0,
                'message': "Bill doesn't exists."
            }
            return Response(data, status=404)

    def delete(self, request, company_id, bill_id):
        """
        An endpoint for deleting bill.
        """
        bill_obj = Bill.objects.filter(id=bill_id, company=company_id)
        if bill_obj:
            try:
                bill_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
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
