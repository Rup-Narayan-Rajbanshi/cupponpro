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
