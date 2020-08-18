from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from commonapp.models.company import Company
from commonapp.models.rating import Rating
from commonapp.serializers.company import CompanySerializer

class CompanyListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CompanySerializer

    def get(self, request):
        company_obj = Company.objects.all()
        serializer = CompanySerializer(company_obj, many=True,\
            context={"request":request})
        for each_serializer in serializer.data:
            company = company_obj.get(id=each_serializer['id'])
            company_images = company.images.all()
            company_images = [request.META['HTTP_HOST'] + '/media/' + str(image.image) for image in company_images]

            rating_obj = Rating.objects.filter(company=company.id)
            rating_count = len(rating_obj)
            rating = 0
            if rating_obj:
                for each_rating_obj in rating_obj:
                    rating += each_rating_obj.rate
                rating /= rating_count

        each_serializer['images'] = company_images
        each_serializer['rating'] = rating
        each_serializer['rating_count'] = rating_count

        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'company': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)
        

class PartnerListView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CompanySerializer

    def get(self, request):
        company_obj = Company.objects.filter(is_partner=True).order_by('-id')
        serializer = CompanySerializer(company_obj, many=True,\
            context={"request":request})
        for each_serializer in serializer.data:
            company = company_obj.get(id=each_serializer['id'])
            company_images = company.images.all()
            company_images = [request.META['HTTP_HOST'] + '/media/' + str(image.image) for image in company_images]

            rating_obj = Rating.objects.filter(company=company.id)
            rating_count = len(rating_obj)
            rating = 0
            if rating_obj:
                for each_rating_obj in rating_obj:
                    rating += each_rating_obj.rate
                rating /= rating_count

        each_serializer['images'] = company_images
        each_serializer['rating'] = rating
        each_serializer['rating_count'] = rating_count

        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)