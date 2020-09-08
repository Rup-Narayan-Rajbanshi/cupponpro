from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.models.category import Category, SubCategory
from commonapp.serializers.category import CategorySerializer, SubCategorySerializer
from permission import isAdminOrReadOnly

class CategoryListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
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
            'message': serializer.errors
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
                'message': "Category doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, category_id):
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            serializer = CategorySerializer(instance=category_obj[0], data=request.data,\
                partial=True, context={'request':request})
            if 'image' in request.data and not request.data['image']:
                serializer.exclude_fields(['image'])
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
                'message': "Category doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, category_id):
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            try:
                category_obj[0].delete()
                data = {
                    'success': 1,
                    'category': 'Category deleted successfully.'
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Category cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Category doesn't exist."
            }
            return Response(data, status=404)

class SubCategoryListView(APIView):
    serializer_class = SubCategorySerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request):
        sub_category_obj = SubCategory.objects.all()
        serializer = SubCategorySerializer(sub_category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'sub_category': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'sub_category': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)

class SubCategoryDetailView(APIView):
    serializer_class = SubCategorySerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request, sub_category_id):
        sub_category_obj = SubCategory.objects.filter(id=sub_category_id)
        if sub_category_obj:
            serializer = SubCategorySerializer(sub_category_obj[0], context={'request':request})
            data = {
                'success': 1,
                'sub_category': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Sub-category doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, sub_category_id):
        sub_category_obj = SubCategory.objects.filter(id=sub_category_id)
        if sub_category_obj:
            serializer = SubCategorySerializer(sub_category_obj[0], data=request.data,\
                partial=True, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'sub_category': serializer.data
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
                'message': "Sub-category doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, sub_category_id):
        sub_category_objj = SubCategory.objects.filter(id=sub_category_id)
        if sub_category_objj:
            sub_category_objj[0].delete()
            data = {
                'success': 1,
                'category': 'Sub-category deleted successfully.'
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Sub-Category doesn't exist."
            }
            return Response(data, status=404)
