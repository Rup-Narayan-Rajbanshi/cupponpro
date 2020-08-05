from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from bannerapp.serializers.banner import BannerSerializer
from bannerapp.models import Banner
from permission import Permission

class BannerListView(APIView):
    permission_classes = (Permission ,)
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
        if request.user.admin:
            serializer = BannerSerializer(data=request.data)
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
        data = {
            'success': 0,
            'message': "You do not have permission to add a banner."
        }
        return Response(data, status=403)


class BannerUpdateView(APIView):
    serializer_class = BannerSerializer

    def get(self, request, banner_id):
        if request.user.admin:
            if Banner.objects.filter(id=banner_id):
                banner_obj = Banner.objects.get(id=banner_id)
                serializer = BannerSerializer(banner_obj,\
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
        data = {
            'success': 0,
            'message': "You do not have permission to get banner."
        }
        return Response(data, status=403)

    def put(self, request, banner_id):
        if request.user.admin:
            if Banner.objects.filter(id=banner_id):
                banner_obj = Banner.objects.get(id=banner_id)
                serializer = BannerSerializer(instance=banner_obj,\
                    data=request.data, partial=True)
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
        data = {
            'success': 0,
            'message': "You do not have permission to add banner."
        }
        return Response(data, status=403)

    def delete(self, request, banner_id):
        if request.user.admin:
            if Banner.objects.filter(id=banner_id):
                banner_obj = Banner.objects.get(id=banner_id)
                banner_obj.delete()
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
        data = {
            'success': 0,
            'message': "You do not have permission to delete banner."
        }
        return Response(data, status=403)