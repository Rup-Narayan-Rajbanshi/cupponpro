from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from permission import isAdminOrReadOnly, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll
from commonapp.models.category import Category
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.company import Company
from commonapp.serializers.coupon import CouponSerializer, VoucherSerializer

class CouponTypeListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]

    def get(self, request):
        coupon_type = {
            'category': 'On all items',
            'productcategory': 'On item type',
            'product': 'On specific item'
        }
        content_type_obj = ContentType.objects.filter(model__in=coupon_type.keys())
        coupon_type_obj = []
        for each_obj in content_type_obj:
            temp = {'id': each_obj.id, 'name': coupon_type[each_obj.model]}
            coupon_type_obj.append(temp)
        data = {
            'success': 1,
            'coupon_type': coupon_type_obj
        }
        return Response(data, status=200)

class CouponListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isAdminOrReadOnly]
    serializer_class = CouponSerializer

    def get(self, request):
        coupon_obj = Coupon.objects.all().order_by('-id')
        serializer = CouponSerializer(coupon_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'coupon' : serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = CouponSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'coupon': serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors,
        }
        return Response(data, status=400)

class CouponDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isAdminOrReadOnly]
    serializer_class = CouponSerializer

    def get(self, request, coupon_id):
        if Coupon.objects.filter(id=coupon_id):
            coupon_obj = Coupon.objects.get(id=coupon_id)
            serializer = CouponSerializer(coupon_obj,\
                context={"request":request})
            data = {
                'success' : 1,
                'coupon' : serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success' : 0,
                "message" : "Coupon doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, coupon_id):
        coupon_obj = Coupon.objects.filter(id=coupon_id)
        if coupon_obj:   
            serializer = CouponSerializer(instance=coupon_obj[0],\
                data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'coupon': serializer.data
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
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, coupon_id):
        coupon_obj = Coupon.objects.filter(id=coupon_id)            
        if coupon_obj:
            try:
                coupon_obj[0].delete()
                data = {
                    'success': 1,
                    'coupon': "Coupon deleted successfully."
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': "Coupon cannot be deleted."
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)

class CategoryCouponListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CouponSerializer

    def get(self, request, category_id):
        company_obj = Company.objects.filter(category=category_id)
        if company_obj:
            coupon_obj = Coupon.objects.filter(company__id__in=company_obj).order_by('-id')
            paginator = Paginator(coupon_obj, 15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if coupon_obj:
                serializer = CouponSerializer(page_obj, many=True, context={"request":request})
                data = {
                    'success': 1,
                    'category': Category.objects.get(id=category_id).name,
                    'coupon': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)

class VoucherListView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = VoucherSerializer

    def get(self, request):
        voucher_obj = Voucher.objects.filter(user=request.user.id).order_by('-id')
        serializer = VoucherSerializer(voucher_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'voucher': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        if request.user.id == int(request.data['user']):
            voucher_obj = Voucher.objects.filter(user=request.user.id, coupon=request.data['coupon'])
            if not voucher_obj:
                serializer = VoucherSerializer(data=request.data, context={'request':request}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'voucher': serializer.data
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
                    'message': "Voucher already exists."
                }
                return Response(data, status=302)
        else:
            data = {
                'success': 0,
                'message': "You do not have permission to generate voucher."
            }
            return Response(data, status=403)