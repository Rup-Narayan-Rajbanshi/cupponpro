from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.product import Product
from commonapp.models.bill import Bill
from commonapp.serializers.bill import BillSerializer
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, isCompanySalePersonAndAllowAll

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
            'data': serializer.data
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
                'data': serializer.data
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

    def get(self, request, bill_id):
        """
        An endpoint for getting bill detail.
        """
        bill_obj = Bill.objects.filter(id=bill_id)
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

class BillVerifyView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll]
    serializer_class = BillSerializer

    def post(self, request):
        """
        An endpoint for bill verification.
        """
        company_id = request.data['company']
        user_id = request.data['user']
        voucher_obj = Voucher.objects.filter(id=request.data['voucher'])
        items = request.data['items']
        if voucher_obj:
            coupon_type = voucher_obj[0].coupon.content_type.model
            product_ids = [x['id'] for x in items]
            # productcategory, category, product
            applicable_products_ids = []
            if coupon_type == "category":
                applicable_products_ids = product_ids
            elif coupon_type == "productcategory":
                product_category_obj = voucher_obj[0].coupon.content_object
                applicable_product_obj = Product.objects.filter(id__in=product_ids, product_category=product_category_obj)
                applicable_products_ids = [str(x.id) for x in applicable_product_obj]
            else:
                applicable_products_ids = str(voucher_obj[0].coupon.object_id)
                applicable_products_ids = [applicable_products_ids]
            # get discount percentage from coupon
            discount_p = voucher_obj[0].coupon.discount
            # loop in items and apply discount
            if applicable_products_ids:
                for item in items:
                    if item['id'] in applicable_products_ids:
                        item['discount'] = discount_p
                        item['voucher'] = str(voucher_obj[0].id)
                        item['total'] = (item['amount'] * item['quantity']) - (discount_p / 100 * (item['amount'] * item['quantity']))
                    else:
                        item['total'] = item['amount']
            data = {
                'success': 1,
                'data': items
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'data': items
            }
            return Response(data, status=200)
