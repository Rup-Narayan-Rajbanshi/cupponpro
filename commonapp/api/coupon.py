from rest_framework.views import APIView
from rest_framework.response import Response
from permission import Permission
from commonapp.models.coupon import Coupon
from commonapp.serializers.coupon import CouponSerializer

class CouponListView(APIView):
    permission_classes = (Permission, )
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
            serializer = CouponSerializer(data=request.data)
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
    permission_classes = (Permission, )
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
                    data=request.data)
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

    def delete(self, request, dcoupon_id):
        if request.user.admin:
            if Coupon.objects.filter(id=dcoupon_id):
                coupon_obj = Coupon.objects.get(id=dcoupon_id)
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