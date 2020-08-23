from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from categoryapp.models.category import Category, ProductCategory
from categoryapp.serializers.category import CategorySerializer, ProductCategorySerializer
from permission import isAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoryListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
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
        serializer = CategorySerializer(data=request.data, context={'request':request})
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

class CategoryDetailView(APIView):
    serializer_class = CategorySerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request, category_id):
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            serializer = CategorySerializer(category_obj[0], context={'request':request})
            data = {
                'success': 1,
                'category': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'Category id not found.'
            }
            return Response(data, status=200)
    
    def put(self, request, category_id):
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            serializer = CategorySerializer(category_obj[0], data=request.data,\
                partial=True, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'category': serializer.data
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
                'message': 'Category id not found.'
            }
            return Response(data, status=400)

    def delete(self, request, category_id):
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            category_obj[0].delete()
            data = {
                'success': 1,
                'category': 'Category deleted successfully.'
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'Category id not found.'
            }
            return Response(data, status=400)

class ProductCategoryListView(APIView):
    permission_classes = (isAdminOrReadOnly ,)
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
