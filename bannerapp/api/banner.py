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
        return Response(serializer.data, status=200)

    def post(self, request):
        if request.user.admin:
            serializer = BannerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({"message":"You do not have permission to add a crm."},\
            status=403)



class BannerUpdateView(APIView):
    serializer_class = BannerSerializer

    def get(self, request, banner_id):
        if request.user.admin:
            if Banner.objects.filter(id=banner_id):
                banner_obj = Banner.objects.get(id=banner_id)
                serializer = BannerSerializer(banner_obj,\
                    context={'request': request})
                return Response(serializer.data)
            return Response({"message":"User id do not match"}, status=400)
        return Response({"message":"You do not have permission to show a user."},\
            status=403)

    def put(self, request, banner_id):
        if request.user.admin:
            if Banner.objects.filter(id=banner_id):
                banner_obj = Banner.objects.get(id=banner_id)
                serializer = BannerSerializer(instance=banner_obj,\
                    data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=200)
                return Response(serializer.errors, status=400)
            return Response({"message":"User id do not match"}, status=400)
        return Response({"message":"You do not have permission to update a crm."},\
            status=403)

    def delete(self, request, banner_id):
        if request.user.admin:
            if Banner.objects.filter(id=banner_id):
                banner_obj = Banner.objects.get(id=banner_id)
                banner_obj.delete()
                return Response({"message":"crm item deleted successfully"},\
                    status=200)
            return Response({"message":"User id do not match"}, status=400)
        return Response({"message":"You do not have permission to delete a crm."},\
            status=403)
