from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from commonapp.models.company import Company, CompanyUser, FavouriteCompany
from commonapp.serializers.company import CompanySerializer, FavouriteCompanySerializer, ChangeCompanyEmailSerializer
from userapp.models.user import User
from userapp.serializers.user import UserDetailSerializer
from permission import isCompanyOwnerAndAllowAll
from helper import isCompanyUser

class CompanyListView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CompanySerializer

    def get(self, request):
        """
        An endpoint for listing all the vendors. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        company_obj = Company.objects.all().order_by('-id')
        paginator = Paginator(company_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CompanySerializer(page_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)

class CompanyDetailView(generics.GenericAPIView):
    serializer_class = CompanySerializer
    permission_classes = (AllowAny, )

    def get(self, request, company_id):
        """
        An endpoint for getting vendor detail.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            serializer = CompanySerializer(company_obj[0], context={'request':request})
            data = {
                'success': 1,
                'company': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'Message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id):
        """
        An endpoint for updating vendor detail.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            serializer = CompanySerializer(instance=company_obj[0], data=request.data,\
                partial=True, context={'request':request})
            if 'logo' in request.data and not request.data['logo']:
                serializer.exclude_fields(['logo'])
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'company': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 1,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'Message': "Company doesn't exist."
            }
            return Response(data, status=404)

class CompanyCreateView(generics.GenericAPIView):
    serializer_class = CompanySerializer
    permission_classes = (isCompanyOwnerAndAllowAll, )

    def post(self, request):
        """
        An endpoint for creating vendor.
        """
        if request.user.id == int(request.data['author']):
            serializer = CompanySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                company_obj = Company.objects.get(id=serializer.data['id'])
                CompanyUser.objects.create(user=request.user, company=company_obj, is_staff=False)
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
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to create company."
            }
            return Response(data, status=403)

class ChangeCompanyEmailView(generics.GenericAPIView):
    serializer_class = ChangeCompanyEmailSerializer
    permission_classes = (isCompanyOwnerAndAllowAll, )

    def put(self, request, company_id):
        """
        An endpoint for changing companies email.
        """
        if isCompanyUser(request.user.id, company_id):
            serializer = ChangeCompanyEmailSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('password')):
                    company_obj = Company.objects.filter(id=company_id)
                    if company_obj:
                        if company_obj[0].email != serializer.data.get('email'):
                            if not Company.objects.filter(email=serializer.data.get('email')):
                                company_obj[0].email = serializer.data.get('email')
                                company_obj[0].save()
                                data = {
                                    'success': 1,
                                    'email': serializer.data.get('email')
                                }
                                return Response(data, status=200)
                            else:
                                data = {
                                    'success': 0,
                                    'message': 'Email is already taken.'
                                }
                                return Response(data, response=400)
                        else:
                            data = {
                                'success': 0,
                                'message': 'Please enter new email.'
                            }
                            return Response(data, status=400)
                    else:
                        data = {
                            'success': 0,
                            'message': 'Company not found.'
                        }
                        return Response(data, status=404)
                else:
                    data = {
                        'success': 0,
                        'message': 'User not verified.'
                    }
                    return Response(data, status=403)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to update email."
            }
            return Response(data, status=403)

class CompanyFavouriteView(generics.GenericAPIView):
    serializer_class = FavouriteCompanySerializer

    def get(self, request, company_id):
        """
        An endpoint for marking vendor as favourite.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            favourite_company_obj, _ = FavouriteCompany.objects.get_or_create(user=request.user, company=company_obj[0])
            serializer = FavouriteCompanySerializer(favourite_company_obj, context={'request':request})
            data = {
                'success': 1,
                'favourtie_company': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id):
        """
        An endpoint for updating vendor as favourite.
        """
        if (int(request.data['user']) == request.user.id) and (int(request.data['company']) == company_id):
            favourite_company_obj = FavouriteCompany.objects.filter(user=request.user, company=company_id)
            if favourite_company_obj:
                serializer = FavouriteCompanySerializer(favourite_company_obj[0], data=request.data,\
                    context={'request':request})
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

class CompanyUserListView(generics.GenericAPIView):
    # permission_classes = () set only company owner and manager to see detail and to admin as well

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's users. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            company_user_obj = CompanyUser.objects.filter(company=company_obj[0])
            # get user data from related company user data
            user_ids = [x.user.id for x in company_user_obj]
            user_obj = User.objects.filter(id__in=user_ids).order_by('-id')
            page_size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(user_obj, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = UserDetailSerializer(page_obj, many=True, context={"request":request})
            for each_serializer in serializer.data:
                del each_serializer['admin']
                each_serializer['staff'] = company_user_obj.get(user__id=each_serializer['id']).is_staff
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
            return Response(data, status=404)

class PartnerListView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CompanySerializer

    def get(self, request):
        """
        An endpoint for listing all the vendor's that are partners. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        company_obj = Company.objects.filter(is_partner=True).order_by('-id')
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(company_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CompanySerializer(page_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'company' : serializer.data,
        }
        return Response(data, status=200)
