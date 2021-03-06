from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from commonapp.models.category import Category
from productapp.models.coupon import Coupon, Voucher
from company.models.company import Company
from productapp.models.product import Product, ProductCategory
from commonapp.serializers.coupon import CouponSerializer, VoucherSerializer, CouponDetailSerializer
from helpers.constants import COUPON_TYPE_MAPPER
from permission import isAdminOrReadOnly, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll ,publicReadOnly
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
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isAdminOrReadOnly | publicReadOnly]
    serializer_class = CouponSerializer

    def get(self, request):
        """
        An endpoint for listing all the coupons. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        filter_fields = ['discount_type', 'name']
        sort_by_fields = ['name', 'expiry_date', 'discount']
        coupon_type = request.GET.get('coupon_type') if request.GET.get('coupon_type') in list(COUPON_TYPE_MAPPER.keys()) else None

        order_by = '' if request.GET.get('order_by') == 'asc' else '-'
        sort_by = request.GET.get('sort_by') if request.GET.get('sort_by') in sort_by_fields else 'id'
        filter_kwargs = {'{key}{lookup}'.format(
            key=key, lookup='__icontains'
            ): value for key, value in request.GET.items() if key in filter_fields}
    
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        try:
            company = request.user.company_user.all().values_list('company', flat=True)[0] 
        except:
            company = request.GET.get('company',None)
        if coupon_type:
            coupon_obj = Coupon.objects.select_related('company').filter(**filter_kwargs,
                                                                         content_type__model=COUPON_TYPE_MAPPER[coupon_type]).order_by(
                '{order_by}{sort_by}'.format(
                    order_by=order_by,
                    sort_by=sort_by
                ))
        else:
            print('here')
            coupon_obj = Coupon.objects.select_related('company').filter(**filter_kwargs).order_by('{order_by}{sort_by}'.format(
                order_by=order_by,
                sort_by=sort_by
            ))

        if company:
            coupon_obj = coupon_obj.filter(company=company)
        paginator = Paginator(coupon_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CouponDetailSerializer(page_obj, many=True, context={"request": request})
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
    serializer_class = CouponDetailSerializer

    def get(self, request, coupon_id):
        """
        An endpoint for getting coupon detail.
        """
        if Coupon.objects.filter(id=coupon_id):
            coupon_obj = Coupon.objects.get(id=coupon_id)
            serializer = CouponDetailSerializer(coupon_obj,\
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
            serializer = CouponDetailSerializer(page_obj, many=True, context={"request":request})
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
        else:
            data = {
                'success': 1,
                'data': []
            }
            return Response(data, status=200)

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

    def post(self, request):
        """
        An endpoint for creating user's voucher.
        """
        if str(request.user.id) == str(request.data.get('user', None)):
            serializer = VoucherSerializer(data=request.data, context={'request':request})
            if not serializer.is_valid():
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)

            voucher_obj = Voucher.objects.filter(user=request.user.id, coupon=request.data['coupon'])
            if not voucher_obj:
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data
                }
                return Response(data, status=200)

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
    serializer_class = CouponDetailSerializer

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
        serializer = CouponDetailSerializer(page_obj, many=True, context={"request":request})
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

class DealOfTheDayCouponListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CouponDetailSerializer

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
        serializer = CouponDetailSerializer(page_obj, many=True, context={"request":request})
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
