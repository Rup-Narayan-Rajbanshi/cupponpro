from rest_framework.response import Response
from rest_framework import generics
from commonapp.models.company import Company, CompanyUser
from commonapp.models.links import SocialLink
from commonapp.serializers.links import SocialLinkSerializer
from permission import isCompanyOwnerAndAllowAll

class SocialLinkListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll]
    serializer_class = SocialLinkSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's social links.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            # check if requesting user belongs to company
            if request.user and request.user.is_authenticated:
                company_user_obj = CompanyUser.objects.filter(user=request.user, company=company_obj[0])
            else:
                company_user_obj = False
            if company_user_obj:
                social_link_obj = SocialLink.objects.filter(company=company_obj[0]).order_by('-id')
                serializer = SocialLinkSerializer(social_link_obj, many=True,\
                    context={"request":request})
                data = {
                    'success' : 1,
                    'social_link' : serializer.data,
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "You do not have permission to view social link."
                }
                return Response(data, status=403)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's social link.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            # check if requesting user belongs to company
            if request.user and request.user.is_authenticated:
                company_user_obj = CompanyUser.objects.filter(user=request.user, company=company_obj[0])
            else:
                company_user_obj = False
            if company_user_obj:
                serializer = SocialLinkSerializer(data=request.data, context={"request":request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success' : 1,
                        'social_link' : serializer.data,
                    }
                    return Response(data, status=200)
                else:
                    data = {
                        'success' : 0,
                        'social_link' : serializer.errors,
                    }
                    return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "You do not have permission to add social link."
                }
                return Response(data, status=403)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

class SocialLinkDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll]
    serializer_class = SocialLinkSerializer

    def get(self, request, company_id, link_id):
        """
        An endpoint for getting vendor's social link detail.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            social_link_obj = SocialLink.objects.filter(id=link_id, company=company_obj[0])
            if social_link_obj:
                serializer = SocialLinkSerializer(social_link_obj[0], context={"request":request})
                data = {
                    'success' : 1,
                    'social_link' : serializer.data,
                }
                return Response(data, status=200)
            else:
                data = {
                    'success' : 0,
                    'message' : 'No such social link found for the company',
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

    def put(self, request, company_id, link_id):
        """
        An endpoint for updating vendor's social link detail.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            social_link_obj = SocialLink.objects.filter(id=link_id, company=company_obj[0])
            if social_link_obj:
                serializer = SocialLinkSerializer(instance=social_link_obj[0], data=request.data, context={"request":request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success' : 1,
                        'social_link' : serializer.data,
                    }
                    return Response(data, status=200)
                else:
                    data = {
                    'success' : 0,
                    'message' : serializer.errors,
                }
                return Response(data, status=400)
            else:
                data = {
                    'success' : 0,
                    'message' : 'No such social link found for the company',
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)
