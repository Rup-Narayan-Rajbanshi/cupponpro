from rest_framework import generics
from rest_framework.response import Response
from commonapp.serializers.company import Company, CompanySerializer
from commonapp.serializers.coupon import Coupon, CouponSerializer
from commonapp.serializers.search import TopBarSearchSerializer

class TopBarSearchView(generics.GenericAPIView):
    serializer_class = TopBarSearchSerializer

    def post(self, request):
        # get data
        company_obj_by_name = Company.objects.filter(name__icontains=request.data['search_text'])
        company_obj_by_location = Company.objects.filter(address__icontains=request.data['search_text'])
        coupon_obj = Coupon.objects.filter(description__icontains=request.data['search_text'])

        # serialize data
        company_by_name_serializer = CompanySerializer(company_obj_by_name, many=True, context={'request':request})
        company_by_location_serializer = CompanySerializer(company_obj_by_location, many=True, context={'request':request})
        coupon_serializer = CouponSerializer(coupon_obj, many=True, context={'request':request})

        data = {
            'success': 1,
            'company_by_name': company_by_name_serializer.data,
            'company_by_location': company_by_location_serializer.data,
            'coupon': coupon_serializer.data,
        }
        return Response(data, status=200)