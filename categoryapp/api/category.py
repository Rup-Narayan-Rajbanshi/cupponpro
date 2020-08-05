from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from categoryapp.models import Category
from categoryapp.serializers.category import CategorySerializer
from permission import Permission


class CategoryListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = CategorySerializer

    def get(self, request):
        category_obj = Category.objects.all()
        serializer = CategorySerializer(category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'category': serializer.data
        }
        return Response(data, status=200)
