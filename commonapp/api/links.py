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

    def delete(self, request, company_id, link_id):
        """
        An endpoint for deleting vendor's social link.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            social_link_obj = SocialLink.objects.filter(id=link_id, company=company_obj[0])
            if social_link_obj:
                try:
                    social_link_obj[0].delete()
                    data = {
                        'success': 1,
                        'social_link': 'Social link deleted successfully.'
                    }
                    return Response(data, status=200)
                except:
                    data = {
                        'success': 0,
                        'message': 'Social link cannot be deleted.'
                    }
                    return Response(data, status=400)
            data = {
                'success': 0,
                'message': "Social link doesn't exist."
            }
            return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist.",
            }
            return Response(data, status=404)

class SocialLinkMassUpdateView(generics.GenericAPIView):
    serializer_class = SocialLinkSerializer

    def put(self, request, company_id):
        """
        An endpoint for updating vendor's social link in mass.
        """
        ids = [x['id'] for x in request.data]
        data = {
            'success': 1,
            'link': [],
            'message': []
        }
        social_link_obj = SocialLink.objects.filter(id__in=ids)
        # mapping social link obj with key, so that during loop, correct data may be accessed even if multiple data are not in sequential order by id
        social_link_obj_dict = dict()
        for obj in social_link_obj:
            social_link_obj_dict[obj.id] = obj
        for r_data in request.data:
            serializer = SocialLinkSerializer(instance=social_link_obj_dict[r_data['id']], data=r_data, context={'request':request})
            if serializer.is_valid():
                # serializer.save()
                data['link'].append(serializer.data)
            else:
                data['message'].append({'id': serializer.instance.id, 'error': serializer.errors})
        return Response(data, status=200)
