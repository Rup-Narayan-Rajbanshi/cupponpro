from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from commonapp.models.company import Company, CompanyUser, FavouriteCompany
from commonapp.models.rating import Rating
from userapp.models.user import User
from commonapp.serializers.company import CompanySerializer, FavouriteCompanySerializer
from userapp.serializers.user import UserDetailSerializer

class CompanyListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CompanySerializer

    def get(self, request):
        company_obj = Company.objects.all()
        serializer = CompanySerializer(company_obj, many=True,\
            context={"request":request})
        for each_serializer in serializer.data:
            company = company_obj.get(id=each_serializer['id'])
            rating_obj = Rating.objects.filter(company=company.id)
            rating_count = len(rating_obj)
            rating = 0
            if rating_obj:
                for each_rating_obj in rating_obj:
                    rating += each_rating_obj.rate
                rating /= rating_count

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

class CompanyFavouriteView(APIView):
    serializer_class = FavouriteCompanySerializer

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            favourite_company_obj, created = FavouriteCompany.objects.get_or_create(user=request.user, company=company_obj[0])
            serializer = FavouriteCompanySerializer(favourite_company_obj)
            data = {
                'success': 1,
                'favourtie_company': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist"
            }
            return Response(data, status=400)

    def put(self, request, company_id):
        if (int(request.data['user']) == request.user.id) and (int(request.data['company']) == company_id):
            favourite_company_obj = FavouriteCompany.objects.filter(user=request.user, company=company_id)
            if favourite_company_obj:
                serializer = FavouriteCompanySerializer(favourite_company_obj[0], data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'favourtie_company': serializer.data
                    }
                    return Response(data, status=200)
                else:
                    data = {
                        'success': 0,
                        'message': serializer.errors
                    }
                    return Response(data, status=400)
        data = {
            'success': 0,
            'message': 'Favourite company data not found.'
        }
        return Response(data, status=400)

class CompanyUserListView(APIView):
    # permission_classes = () set only company owner and manager to see detail and to admin as well

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            company_user_obj = CompanyUser.objects.filter(company=company_obj[0])
            # get user data from related company user data
            user_ids = [x.user.id for x in company_user_obj]
            user_obj = User.objects.filter(id__in = user_ids)
            serializer = UserDetailSerializer(user_obj, many=True)
            for each_serializer in serializer.data:
                del each_serializer['admin']
                each_serializer['staff'] = company_user_obj.get(user__id =each_serializer['id']).is_staff
                
            data = {
                'success': 1,
                'user': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
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
            rating_obj = Rating.objects.filter(company=company.id)
            rating_count = len(rating_obj)
            rating = 0
            if rating_obj:
                for each_rating_obj in rating_obj:
                    rating += each_rating_obj.rate
                rating /= rating_count

            each_serializer['rating'] = rating
            each_serializer['rating_count'] = rating_count

        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)