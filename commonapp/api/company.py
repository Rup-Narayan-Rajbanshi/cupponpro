import math
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from commonapp.models.company import Company, CompanyUser, FavouriteCompany
from commonapp.serializers.company import CompanySerializer, FavouriteCompanySerializer, ChangeCompanyEmailSerializer
from userapp.models.user import User
from userapp.serializers.user import UserDetailSerializer
from permission import isCompanyOwnerAndAllowAll, publicReadOnly
from helper import isCompanyUser
from commonapp.models.coupon import Coupon
from commonapp.serializers.coupon import CouponSerializer, CouponDetailSerializer
from django.db.models import (
    F,
    FloatField,
    Q,
    Value,
    Avg,
    Count,
    IntegerField
)
from django.db.models.functions import Coalesce


class CompanyListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | publicReadOnly]
    serializer_class = CompanySerializer

    def get(self, request):
        """
        An endpoint for listing all the vendors. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        search = request.GET.get('search')
        filter_by = request.GET.get('filter_by')
        company_obj = Company.objects.annotate(
                            rating = Coalesce(
                                Avg(
                                    F("company_rating__rate"),
                                    output_field=FloatField(),
                                ),
                                Value(0),
                            ),
                            rating_count = Coalesce(
                                Count(
                                    F("company_rating"),
                                    output_field=IntegerField(),
                                ),
                                Value(0),
                            )
                        ).all().order_by('-id')
        if search:
            company_obj = company_obj.filter(name__istartswith=search)
        if filter_by == 'top_rated':
            company_obj = company_obj.order_by('-rating', '-id')
        paginator = Paginator(company_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CompanySerializer(page_obj, many=True,\
            context={"request":request})
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
            'data': serializer.data,
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating vendor.
        """
        if str(request.user.id) == str(request.data.get('author', None)):
            serializer = CompanySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                company_obj = Company.objects.get(id=serializer.data['id'])
                CompanyUser.objects.create(user=request.user, company=company_obj, is_staff=False)
                data = {
                    'success': 1,
                    'data': serializer.data
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

class CompanyDetailView(generics.GenericAPIView):
    serializer_class = CompanySerializer
    permission_classes = (AllowAny, )

    def get(self, request, company_id):
        """
        An endpoint for getting vendor detail.
        """
        company_obj = Company.objects.filter(id=company_id).annotate(
                            rating = Coalesce(
                                Avg(
                                    F("company_rating__rate"),
                                    output_field=FloatField(),
                                ),
                                Value(0),
                            ),
                            rating_count = Coalesce(
                                Count(
                                    F("company_rating"),
                                    output_field=IntegerField(),
                                ),
                                Value(0),
                            )
                        )
        if company_obj:
            serializer = CompanySerializer(company_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
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
                    'data': serializer.data
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

class ChangeCompanyEmailView(generics.GenericAPIView):
    serializer_class = ChangeCompanyEmailSerializer
    permission_classes = (isCompanyOwnerAndAllowAll, )

    def put(self, request, company_id):
        """
        An endpoint for changing company's email.
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
                                    'data': None
                                }
                                return Response(data, status=200)
                            else:
                                data = {
                                    'success': 0,
                                    'message': 'Email is already taken.'
                                }
                                return Response(data, status=400)
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
    permission_classes = (IsAuthenticated, )

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
                'data': serializer.data
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
        favourite_company_obj = FavouriteCompany.objects.filter(user=request.user, company=company_id)
        if favourite_company_obj:
            serializer = FavouriteCompanySerializer(favourite_company_obj[0], data=request.data,\
                context={'request':request})
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
        data = {
            'success': 0,
            'message': 'Favourite company data not found.'
        }
        return Response(data, status=404)

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
            print("here")
            print(user_obj)
            page_size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(user_obj, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = UserDetailSerializer(page_obj, many=True, context={"request":request})
            for each_serializer in serializer.data:
                del each_serializer['admin']
                each_serializer['staff'] = company_user_obj.get(user__id=each_serializer['id']).is_staff
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
        company_obj = Company.objects.filter(is_partner=True).annotate(
                            rating = Coalesce(
                                Avg(
                                    F("company_rating__rate"),
                                    output_field=FloatField(),
                                ),
                                Value(0),
                            ),
                            rating_count = Coalesce(
                                Count(
                                    F("company_rating"),
                                    output_field=IntegerField(),
                                ),
                                Value(0),
                            )
                        ).order_by('-id')
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(company_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CompanySerializer(page_obj, many=True,\
            context={"request":request})
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
            'data': serializer.data,
        }
        return Response(data, status=200)

class CategoryCompanyListView(generics.GenericAPIView):
    permission_classes = (publicReadOnly, )
    serializer_class = CompanySerializer

    def get(self, request, category_id):
        """
        An endpoint for listing all the company according to category. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        company_obj = Company.objects.filter(category=category_id).annotate(
                            rating = Coalesce(
                                Avg(
                                    F("company_rating__rate"),
                                    output_field=FloatField(),
                                ),
                                Value(0),
                            ),
                            rating_count = Coalesce(
                                Count(
                                    F("company_rating"),
                                    output_field=IntegerField(),
                                ),
                                Value(0),
                            )
                        ).order_by('-id')
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        paginator = Paginator(company_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = CompanySerializer(page_obj, many=True, context={"request":request})
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


class CompanyCouponListView(generics.GenericAPIView):
    permission_classes = (publicReadOnly, )
    serializer_class = CouponDetailSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the company's coupon.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            company_coupon_obj = Coupon.objects.filter(company=company_obj[0])
            # get coupon data from related company data
            coupon_ids = [x.id for x in company_coupon_obj]
            coupon_obj = Coupon.objects.filter(id__in=coupon_ids).order_by('-id')
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
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

class LocalRestaurantListView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CouponDetailSerializer

    def get(self, request):
        """
        An endpoint for listing all the local that are near to user. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively. Pass 'longitude' and 'latitude' and 'distance' (distance is optional and 5 km is taken as default distance) as query.
        Pass 'Restaurant' or 'Hotel' as value to 'category' query to get local restaurant or hotel accordingly.
        """
        try:
            latitude = float(request.GET.get('latitude', None))
            longitude = float(request.GET.get('longitude', None))
            distance = float(request.GET.get('distance', 5))
            category = request.GET.get('category', None)
        except Exception as e:
            latitude = None
            longitude = None
            category = None
        if latitude and longitude and category:
            threshold_latitude = distance / 110.574
            threshold_longitude = distance / (111.320 * math.cos(latitude / math.pi / 180))
            latitude_p = latitude + threshold_latitude
            latitude_m = latitude - threshold_latitude
            longitude_p = longitude + threshold_longitude
            longitude_m = longitude - threshold_longitude
            category_Q = Q(category__name=category)
            distance_Q = (Q(latitude__range=[latitude_m,latitude_p]) & Q(longitude__range=[longitude_m,longitude_p]))
            company_obj = Company.objects.filter(category_Q & distance_Q).order_by('-id').values_list('id', flat=True)
            coupons = Coupon.objects.select_related('company').filter(company__in=company_obj)
            page_size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            paginator = Paginator(coupons, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = self.get_serializer(page_obj, many=True,\
                context={"request":request})
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
                'data': serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'previous_page': None,
                'next_page': None,
                'page_count': None,
                'data': [],
            }
            return Response(data, status=200)
