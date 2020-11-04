from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.models.bill import Bill
from commonapp.models.coupon import Voucher
from commonapp.models.product import Product
from commonapp.models.salesitem import SalesItem
from commonapp.serializers.bill import BillSerializer
from commonapp.serializers.salesitem import SalesItemSerializer
from permission import isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, isCompanySalePersonAndAllowAll

class SalesItemListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = SalesItemSerializer

    def get(self, request, company_id, bill_id):
        """
        An endpoint for listing all the salesitem of the bill.
        """
        sales_item_obj = SalesItem.objects.filter(bill=bill_id)
        if sales_item_obj:
            serializer = SalesItemSerializer(sales_item_obj, many=True, context={'request':request})
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

class SalesItemDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll]
    serializer_class = SalesItemSerializer

    def get(self, request, company_id, bill_id, item_id):
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
                'success': 0,
                'message': "Sales Item doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id, bill_id, item_id):
        """
        An endpoint for updating salesitem.
        """
        item_obj = SalesItem.objects.filter(id=item_id, bill=bill_id)
        if item_obj:
            serializer = SalesItemSerializer(instance=item_obj[0], data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                bill_obj = Bill.objects.get(id=item_obj[0].bill_id)
                serializer = BillSerializer(bill_obj, context={'request':request})
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
                'success': 0,
                'message': "Sales Item doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, company_id, bill_id, item_id):
        """
        An endpoint for deleting salesitem.
        """
        item_obj = SalesItem.objects.filter(id=item_id, bill=bill_id)
        if item_obj:
            try:
                item_obj[0].delete()
                bill_obj = Bill.objects.get(id=bill_id)
                serializer = BillSerializer(bill_obj, context={'request':request})
                data = {
                    'success': 1,
                    'data': serializer.data
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

class SalesItemVerifyView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll]
    serializer_class = SalesItemSerializer

    def post(self, request, company_id):
        """
        An endpoint for sale item verification.
        """
        voucher_obj = Voucher.objects.filter(id=request.data['voucher'])
        items = request.data['items']
        result = {
            'tax': request.data['tax'],
            'taxed_amount': None,
            'total': None,
            'grand_total': None,
            'discount': None,
            'sales_item': items
        }
        if voucher_obj:
            coupon_type = voucher_obj[0].coupon.content_type.model
            product_ids = [x['product'] for x in items]
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
                for item in items:
                    if item['product'] in applicable_products_ids:
                        item['discount'] = discount_p
                        item['voucher'] = str(voucher_obj[0].id)
                        item['total'] = (item['rate'] * item['quantity']) - (discount_p / 100 * (item['rate'] * item['quantity']))
                    else:
                        item['total'] = item['rate'] * item['quantity']
                    total += item['total']
            result['total'] = total
            result['grand_total'] = total
            if result['tax']:
                result['taxed_amount'] = result['tax']/100*result['total']
                result['grand_total'] = result['total'] + result['taxed_amount']      
            result['sales_item'] = items
            data = {
                'success': 1,
                'data': result
            }
            return Response(data, status=200)
        else:
            total = 0
            for item in items:
                item['total'] = item['rate'] * item['quantity']
                total += item['total']
            result['total'] = total
            result['grand_total'] = total
            if result['tax']:
                result['taxed_amount'] = result['tax']/100*result['total']
                result['grand_total'] = result['total'] + result['taxed_amount']
            data = {
                'success': 1,
                'data': result
            }
            return Response(data, status=200)
