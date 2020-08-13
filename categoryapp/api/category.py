from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from categoryapp.models.category import Category, ProductCategory
from categoryapp.serializers.category import CategorySerializer, ProductCategorySerializer
from permission import Permission
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoryListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        category_obj = Category.objects.all()
        serializer = CategorySerializer(category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'category': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'category': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'category': serializer.errors
        }
        return Response(data, status=400)

class ProductCategoryListView(APIView):
    permission_classes = (Permission ,)
    serializer_class = ProductCategorySerializer

    def get(self, request):
        product_category_obj = ProductCategory.objects.all()
        serializer = CategorySerializer(product_category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'productcategory': serializer.data
        }
        return Response(data, status=200)
