from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from commonapp.models.bill import Bill
from commonapp.models.company import Company
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
        items = request.data['sales_item']
        company_obj = Company.objects.filter(id=company_id)
        result = {
            'user': request.data.get('user'),
            'name': request.data.get('name'),
            'phone_number': request.data.get('phone_number'),
            'email': request.data.get('email'),
            'tax': company_obj[0].tax,
            'taxed_amount': 0,
            'service_charge': company_obj[0].service_charge,
            'service_charge_amount': 0,
            'total': 0,
            'grand_total': 0,
            'discount_amount': 0,
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
                        item['discount_amount'] = (discount_p / 100 * (item['rate'] * item['quantity']))
                        item['total'] = (item['rate'] * item['quantity']) - item['discount_amount']
                        result['discount_amount'] += item['discount_amount']
                    else:
                        item['total'] = item['rate'] * item['quantity']
                    total += item['total']
            result['total'] = total
            if result['tax']:
                result['taxed_amount'] = float(result['tax'])/100*float(result['total'])
            if result['service_charge']:
                result['service_charge_amount'] = float(result['service_charge'])/100*float(result['total'])
            result['grand_total'] = result['total'] + result['taxed_amount'] + result['service_charge_amount']
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
