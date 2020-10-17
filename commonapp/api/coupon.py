from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from commonapp.models.category import Category
from commonapp.models.coupon import Coupon, Voucher
from commonapp.models.company import Company
from commonapp.serializers.coupon import CouponSerializer, VoucherSerializer
from permission import isAdminOrReadOnly, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll
from datetime import datetime

class CouponTypeListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]

    def get(self, request):
        """
        An endpoint for listing all coupon types.
        """
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
            'data': coupon_type_obj
        }
        return Response(data, status=200)

class CouponListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isAdminOrReadOnly]
    serializer_class = CouponSerializer

    def get(self, request):
        """
        An endpoint for listing all the coupons. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        coupon_obj = Coupon.objects.all().order_by('-id')
        paginator = Paginator(coupon_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CouponSerializer(page_obj, many=True,\
            context={"request":request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating coupon.
        """
        serializer = CouponSerializer(data=request.data, context={'request':request})
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

class CouponDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isAdminOrReadOnly]
    serializer_class = CouponSerializer

    def get(self, request, coupon_id):
        """
        An endpoint for getting coupon detail.
        """
        if Coupon.objects.filter(id=coupon_id):
            coupon_obj = Coupon.objects.get(id=coupon_id)
            serializer = CouponSerializer(coupon_obj,\
                context={"request":request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                "message": "Coupon doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, coupon_id):
        """
        An endpoint for updating coupon detail.
        """
        coupon_obj = Coupon.objects.filter(id=coupon_id)
        if coupon_obj:   
            serializer = CouponSerializer(instance=coupon_obj[0],\
                data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
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
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, coupon_id):
        """
        An endpoint for deleting coupon.
        """
        coupon_obj = Coupon.objects.filter(id=coupon_id)            
        if coupon_obj:
            try:
                coupon_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
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
        """
        An endpoint for listing all the coupons according to category. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        company_obj = Company.objects.filter(category=category_id)
        if company_obj:
            coupon_obj = Coupon.objects.filter(company__id__in=company_obj).order_by('-id')
            page_size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(coupon_obj, page_size)
            page_obj = paginator.get_page(page_number)
            if coupon_obj:
                serializer = CouponSerializer(page_obj, many=True, context={"request":request})
                data = {
                    'success': 1,
                    'data': serializer.data
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
        """
        An endpoint for listing all the user's vouchers. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        voucher_obj = Voucher.objects.filter(user=request.user.id).order_by('-id')
        paginator = Paginator(voucher_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = VoucherSerializer(page_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating user's voucher.
        """
        if request.user.id == int(request.data['user']):
            voucher_obj = Voucher.objects.filter(user=request.user.id, coupon=request.data['coupon'])
            if not voucher_obj:
                serializer = VoucherSerializer(data=request.data, context={'request':request}, partial=True)
                if serializer.is_valid():
                    serializer.save()
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
                    'message': "Voucher already exists."
                }
                return Response(data, status=302)
        else:
            data = {
                'success': 0,
                'message': "You do not have permission to generate voucher."
            }
            return Response(data, status=403)

class TrendingCouponListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CouponSerializer

    def get(self, request):
        """
        An endpoint for listing all the trending coupons. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        coupon_obj = Coupon.objects.filter(expiry_date__gte=datetime.date(datetime.now())).order_by('-id')
        coupon_count_list = list()
        # counting coupon redeemed
        for coupon in coupon_obj:
            coupon_redeemed_count = Voucher.objects.filter(coupon=coupon).count()
            coupon_count_list.append([coupon_redeemed_count, coupon])
        # sort coupon
        coupon_count_list.sort(key = lambda x: x[0], reverse=True)
        # create coupon obj from sorted data
        coupon_obj = [x[1] for x in coupon_count_list]
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(coupon_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CouponSerializer(page_obj, many=True, context={"request":request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

class DealOfTheDayCouponListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CouponSerializer

    def get(self, request):
        """
        An endpoint for listing all the deals of the day coupons. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        coupon_obj = Coupon.objects.filter(expiry_date__gte=datetime.date(datetime.now()), deal_of_the_day=True).order_by('-id')
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(coupon_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CouponSerializer(page_obj, many=True, context={"request":request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)
