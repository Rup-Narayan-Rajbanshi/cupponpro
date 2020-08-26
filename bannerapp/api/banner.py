from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from bannerapp.serializers.banner import BannerSerializer
from bannerapp.models.banner import Banner
from permission import isAdminOrReadOnly

class BannerListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = BannerSerializer

    def get(self, request):
        banner_obj = Banner.objects.all()
        serializer = BannerSerializer(banner_obj, many=True,\
            context={"request":request})
        data = {
            'success': 1,
            'banner': serializer.data,
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = BannerSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'banner': serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors,
        }
        return Response(data, status=400)


class BannerUpdateView(APIView):
    serializer_class = BannerSerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request, banner_id):
        banner_obj = Banner.objects.filter(id=banner_id)
        if banner_obj:
            serializer = BannerSerializer(banner_obj[0],\
                context={'request': request})
            data = {
                'success': 1,
                'banner': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "Banner id not found."
        }
        return Response(data, status=400)

    def put(self, request, banner_id):
        banner_obj = Banner.objects.filter(id=banner_id)
        if banner_obj:
            serializer = BannerSerializer(instance=banner_obj[0],\
                data=request.data, partial=True, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'banner': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "Banner id not found."
        }
        return Response(data, status=400)

    def delete(self, request, banner_id):
        banner_obj = Banner.objects.filter(id=banner_id)
        if banner_obj:
            banner_obj[0].delete()
            data = {
                'success': 1,
                'banner': "Banner deleted successfully."
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "Banner id not found."
        }
        return Response(data, status=400)