from rest_framework import generics
from rest_framework.response import Response
from commonapp.models.affiliate import AffiliateLink
from commonapp.serializers.affiliate import AffiliateLinkSerializer
from permission import isAdminOrReadOnly

class AffiliateLinkListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = AffiliateLinkSerializer

    def get(self, request):
        affiliate_link_obj = AffiliateLink.objects.all().order_by('-id')
        serializer = AffiliateLinkSerializer(affiliate_link_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'affiliate_link': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = AffiliateLinkSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'affiliate_link': serializer.data
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
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            serializer = AffiliateLinkSerializer(affiliate_link_obj[0], context={"request": request})
            data = {
                'success': 1,
                'affiliate_link': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Affiliate link doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, affiliate_link_id):
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
                    'affiliate_link': serializer.data
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
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            try:
                affiliate_link_obj[0].delete()
                data = {
                    'success': 1,
                    'affiliate_link': "Affiliate link deleted successfully."
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
        affiliate_link_obj = AffiliateLink.objects.filter(id=affiliate_link_id)
        if affiliate_link_obj:
            affiliate_link_obj[0].add_count()
            serializer = AffiliateLinkSerializer(affiliate_link_obj[0], context={'request':request})
            data = {
                'success': 1,
                'affiliate_link': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "Affiliate link doesn't exist."
            }
            return Response(data, status=404)