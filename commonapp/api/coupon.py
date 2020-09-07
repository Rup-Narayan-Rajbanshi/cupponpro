from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from permission import isAdminOrReadOnly, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll
from commonapp.models.category import Category
from commonapp.models.coupon import Coupon
from commonapp.models.company import Company
from commonapp.serializers.coupon import CouponSerializer

class CouponTypeListView(APIView):
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

class CouponListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
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
                "message" : "Coupon doesn't exist."
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
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)
        data = {
            'success': 0,
            'message': "You do not have permission to update coupon."
        }
        return Response(data, status=403)

    def delete(self, request, coupon_id):
        if request.user.admin:
            if Coupon.objects.filter(id=coupon_id):
                coupon_obj = Coupon.objects.get(id=coupon_id)
                if coupon_obj:
                    try:
                        coupon_obj.delete()
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