from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from commonapp.models.bill import Bill
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.product import Product
from commonapp.models.order import Order
from commonapp.serializers.bill import BillSerializer, BillSaveSerializer, BillUserDetailSerializer
from userapp.models.user import User
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
        # bill_obj = Bill.objects.filter(company=company_id)

        filter_fields = ['invoice_number', 'created_at', 'customer_name', 'status']
        sort_by_fields = ['invoice_number', 'created_at', 'customer_name', 'status', 'paid_amount']

        sort_by = request.GET.get('sort_by') if request.GET.get('sort_by') in sort_by_fields else 'id'
        sort_by = 'name__icontains' if sort_by == 'customer_name' else sort_by
        order_by = '' if request.GET.get('order_by') == 'asc' else '-'

        filter_kwargs = {'{key}{lookup}'.format(
            key=key, lookup='__icontains'
            ): value for key, value in request.GET.items() if key in filter_fields}

        if 'customer_name__icontains' in filter_kwargs.keys():
            filter_kwargs['name__icontains'] = filter_kwargs['customer_name__icontains']
            del filter_kwargs['customer_name__icontains']

        bill_obj = Bill.objects.filter(**filter_kwargs, company=company_id).order_by(
            '{order_by}{sort_by}'.format(
                order_by=order_by,
                sort_by=sort_by
            ))

        paginator = Paginator(bill_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = BillSerializer(page_obj, many=True,\
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

    def post(self,request, company_id):
        """
        An endpoint for creating bill.
        """
        order_id = request.data.get('order', None)
        serializer = BillSaveSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            # renaming sales into sales_item
            temp_data = dict(serializer.data)
            sales_item = temp_data.pop('sales')
            temp_data['sales_item'] = sales_item
            # mark order as billed
            if order_id:
                Order.objects.filter(id=order_id).update(is_billed=True)
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
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
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
            serializer = BillSaveSerializer(instance=bill_obj[0], data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                # this step is necessary or else obj parameter in BillSaveSerializer won't get bill obj
                serializer = BillSaveSerializer(bill_obj[0], context={'request':request})
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

class BillUserDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BillUserDetailSerializer

    def post(self, request):
        """
        An endpoint for getting billing user's detail. Pass 'company' as get parameter that holds company id.
        """
        email = request.data.get('email', None)
        phone_number = request.data.get('phone_number', None)
        if email and phone_number:
            query = Q(email=email) | Q(phone_number__contains=phone_number)
        elif email:
            query = Q(email=email)
        elif phone_number:
            query = Q(phone_number__contains=phone_number)
        else:
            data = {
                'success': 0,
                'message': "Enter either phone number or email."
            }
            return Response(data, status=400)

        user_obj = User.objects.filter(query)
        if user_obj:
            serializer = BillUserDetailSerializer(user_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'data': request.data
            }
            return Response(data, status=200)
