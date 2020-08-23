from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from permission import isAdminOrReadOnly
from categoryapp.models.category import Category
from commonapp.models.coupon import Coupon
from commonapp.models.company import Company
from commonapp.serializers.coupon import CouponSerializer

class CouponListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CouponSerializer

    def get(self, request):
        coupon_obj = Coupon.objects.all()
        serializer = CouponSerializer(coupon_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'coupon' : serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        if request.user.admin:
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
        data = {
            'success': 0,
            'message': "You do not have permission to add a coupon."
        }
        return Response(data, status=403)

class CouponDetailView(APIView):
    permission_classes = (isAdminOrReadOnly, )
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
                "message" : "Coupon id not found."
            }
            return Response(data, status=404)

    def put(self, request, coupon_id):
        if request.user.admin:
            if Coupon.objects.filter(id=coupon_id):
                coupon_obj = Coupon.objects.get(id=coupon_id)
                serializer = CouponSerializer(instance=coupon_obj,\
                    data=request.data, context={'request':request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'coupon': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': "Coupon id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to update coupon."
        }
        return Response(data, status=403)

    def delete(self, request, coupon_id):
        if request.user.admin:
            if Coupon.objects.filter(id=coupon_id):
                coupon_obj = Coupon.objects.get(id=coupon_id)
                coupon_obj.delete()
                data = {
                    'success': 1,
                    'coupon': "Coupon deleted successfully."
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': "Coupon id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to delete Coupon."
        }
        return Response(data, status=403)

class CategoryCouponListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CouponSerializer

    def get(self, request, category_id):
        company_obj = Company.objects.filter(category=category_id)
        if company_obj:
            coupon_obj = Coupon.objects.filter(company__id__in=company_obj).order_by('-id')
            paginator = Paginator(coupon_obj,15)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            if coupon_obj:
                serializer = CouponSerializer(page_obj, many=True, context={"request":request})
                data = {
                    'success': 1,
                    'category': Category.objects.get(id=category_id).name,
                    'coupon': serializer.data,                    
                }
                return Response(data, status=200)
            data = {
                'success' : 0,
                'message' : 'No coupon found.',
            }
            return Response(data, status=400)
        else:
            data = {
                'success' : 0,
                'coupon' : 'No coupon found',
            }
            return Response(data, status=400)