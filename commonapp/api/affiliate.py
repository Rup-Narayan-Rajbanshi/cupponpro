from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from commonapp.models.affiliate import AffiliateLink
from commonapp.serializers.affiliate import AffiliateLinkSerializer
from permission import isAdminOrReadOnly

class AffiliateLinkListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = AffiliateLinkSerializer

    def get(self, request):
        """
        An endpoint for listing all the affiliate links. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        affiliate_link_obj = AffiliateLink.objects.all().order_by('-id')
        paginator = Paginator(affiliate_link_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = AffiliateLinkSerializer(page_obj, many=True,\
            context={"request": request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating affiliate link.
        """
        serializer = AffiliateLinkSerializer(data=request.data, context={"request": request})
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

class AffiliateLinkDetailView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = AffiliateLinkSerializer

    def get(self, request, affiliate_link_id):
        """
        An endpoint for getting affiliate link detail.
        """
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            serializer = AffiliateLinkSerializer(affiliate_link_obj[0], context={"request": request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Affiliate link doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, affiliate_link_id):
        """
        An endpoint for updating affiliate link detail.
        """
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            serializer = AffiliateLinkSerializer(instance=affiliate_link_obj[0], data=request.data,\
                partial=True, context={"request": request})
            if 'image' in request.data and not request.data['image']:
                serializer.exclude_fields(['image'])
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
        else:
            data = {
                'success': 0,
                'message': "Affiliate link doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, affiliate_link_id):
        """
        An endpoint for deleting affiliate link.
        """
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            try:
                affiliate_link_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': "Affiliate link cannot be deleted."
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Affiliate link doesn't exist."
            }
            return Response(data, status=404)

class AffiliateLinkCountView(generics.GenericAPIView):
    serializer_class = AffiliateLinkSerializer

    def get(self, request, affiliate_link_id):
        """
        An endpoint for making increment in affiliate link click count.
        """
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            affiliate_link_obj[0].add_count()
            serializer = AffiliateLinkSerializer(affiliate_link_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Affiliate link doesn't exist."
            }
            return Response(data, status=404)

class TopDiscountAffiliateListView(generics.GenericAPIView):
    serializer_class = AffiliateLinkSerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request):
        """
        An endpoint for listing all the affiliate link sorted by discount in descending order.\
        Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10)
        page_number = request.GET.get('page')
        affiliate_link_obj = AffiliateLink.objects.filter(is_active=True).order_by('-discount')
        paginator = Paginator(affiliate_link_obj, page_size)
        page_obj = paginator.get_page(page_number)
        serializer = AffiliateLinkSerializer(page_obj, many=True,\
            context={"request": request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)
