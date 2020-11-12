from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.models.order import Order, OrderLine
from commonapp.models.product import Product
from commonapp.serializers.bill import BillUserDetailSerializer
from commonapp.serializers.order import OrderSerializer, OrderSaveSerializer,OrderLineSerializer
from userapp.models.user import User
from helper import isCompanyUser
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, isCompanySalePersonAndAllowAll, publicReadOnly

class OrderListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll | AllowAny]
    serializer_class = OrderSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the orders. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        order_obj = Order.objects.all()
        paginator = Paginator(order_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = OrderSerializer(page_obj, many=True,\
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
        An endpoint for creating order.
        """
        serializer = OrderSaveSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            # renaming order into order_lines
            temp_data = dict(serializer.data)
            order_lines = temp_data.pop('order')
            temp_data['order_lines'] = order_lines
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

class OrderDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll | AllowAny]
    serializer_class = OrderSerializer

    def get(self, request, company_id, order_id):
        """
        An endpoint for getting order detail.
        """
        order_obj = Order.objects.filter(id=order_id, company=company_id)
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

    def put(self,request, company_id, order_id):
        """
        An endpoint for updating bill.
        """
        order_obj = Order.objects.filter(id=order_id, company=company_id)
        if order_obj:
            serializer = OrderSaveSerializer(instance=order_obj[0], data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                # this step is necessary or else obj parameter in OrderSaveSerializer won't get order obj
                serializer = OrderSerializer(order_obj[0], context={'request':request})
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
                'message': "Order doesn't exists."
            }
            return Response(data, status=404)

    def delete(self, request, company_id, order_id):
        """
        An endpoint for deleting order.
        """
        order_obj = Order.objects.filter(id=order_id, company=company_id)
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
        order_obj = Order.objects.filter(company=company_id, is_billed=False)
        serializer = OrderSerializer(order_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

class OrderUserDetailView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = BillUserDetailSerializer

    def post(self, request):
        """
        An endpoint for getting ordering user's detail. Pass 'company' as get parameter that holds company id.
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

class OrderToBillView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll]

    def get(self, request, company_id):
        """
        An endpoint for converting vendor's active order into billable sales item.
        """
        bill = request.data
        bill['payment_mode'] = 'Cash'
        bill.pop('asset')
        bill.pop('asset_name')
        bill.pop('is_billed')
        bill['order'] = bill.pop('id')

        for order in bill['order_lines']:
            if order['state'] != 'Cancelled':
                order.pop('state')
                order['order'] = order.pop('id')
                order['discount'] = None
                order['total'] = order['rate'] * order['quantity']
                order['voucher'] = None
        bill['sales_item'] = bill.pop('order_lines')
        data = {
            'success': 1,
            'data': bill
        }
        return Response(data, status=200)

class OrderLineVerifyView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderLineSerializer

    def post(self, request, company_id):
        """
        An endpoint for sale item verification.
        """
        voucher_obj = Voucher.objects.filter(id=request.data['voucher'])
        order_lines = request.data['order_lines']
        company_obj = Company.objects.filter(id=request.data['company'])
        result = {
            'tax': company_obj[0].tax,
            'taxed_amount': 0,
            'service_charge': company_obj[0].service_charge,
            'service_charge_amount': 0,
            'total': 0,
            'grand_total': 0,
            'discount_amount': 0,
            'order_lines': order_lines
        }
        if voucher_obj:
            coupon_type = voucher_obj[0].coupon.content_type.model
            product_ids = [x['product'] for x in order_lines]
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
                total = 0
                for item in order_lines:
                    if item['product'] in applicable_products_ids:
                        item['discount'] = discount_p
                        item['voucher'] = str(voucher_obj[0].id)
                        item['discount_amount'] = discount_p / 100 * (item['rate'] * item['quantity'])
                        item['total'] = (item['rate'] * item['quantity']) - item['discount_amount']
                        result['discount_amount'] += item['discount_amount']
                    else:
                        item['total'] = item['rate'] * item['quantity']
                    total += item['total']
            result['total'] = total
            result['grand_total'] = total
            if result['tax']:
                result['taxed_amount'] = float(result['tax'])/100*float(result['total'])  
            if result['service_charge']:
                result['service_charge_amount'] = float(result['service_charge'])/100*float(result['total'])
            result['grand_total'] = result['total'] + result['taxed_amount'] + result['service_charge_amount']      
            result['order_lines'] = order_lines
            data = {
                'success': 1,
                'data': result
            }
            return Response(data, status=200)
        else:
            total = 0
            for item in order_lines:
                item['total'] = item['rate'] * item['quantity']
                total += item['total']
            result['total'] = total
            if result['tax']:
                result['taxed_amount'] = float(result['tax'])/100*float(result['total'])  
            if result['service_charge']:
                result['service_charge_amount'] = float(result['service_charge'])/100*float(result['total'])
            result['grand_total'] = result['total'] + result['taxed_amount'] + result['service_charge_amount']
            data = {
                'success': 1,
                'data': result
            }
            return Response(data, status=200)
