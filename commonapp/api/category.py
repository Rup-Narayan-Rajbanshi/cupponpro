from rest_framework import generics
from rest_framework.response import Response
from commonapp.models.category import Category, SubCategory
from commonapp.serializers.category import CategorySerializer, SubCategorySerializer
from permission import isAdminOrReadOnly

class CategoryListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = CategorySerializer

    def get(self, request):
        """
        An endpoint for listing all the categories.
        """
        category_obj = Category.objects.all()
        serializer = CategorySerializer(category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating category.
        """
        serializer = CategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)

class CategoryDetailView(generics.GenericAPIView):
    serializer_class = CategorySerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request, category_id):
        """
        An endpoint for getting category detail.
        """
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            serializer = CategorySerializer(category_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Category doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, category_id):
        """
        An endpoint for updating category detail.
        """
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            serializer = CategorySerializer(instance=category_obj[0], data=request.data,\
                partial=True, context={'request':request})
            exclude_fields = []
            if 'image' in request.data and not request.data['image']:
                exclude_fields.append('image')
            if 'icon' in request.data and not request.data['icon']:
                exclude_fields.append('icon')
            if exclude_fields:
                serializer.exclude_fields(exclude_fields)
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
                'message': "Category doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, category_id):
        """
        An endpoint for deleting category.
        """
        category_obj = Category.objects.filter(id=category_id)
        if category_obj:
            try:
                category_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
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

class SubCategoryListView(generics.GenericAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request):
        """
        An endpoint for listing all the sub-category.
        """
        sub_category_obj = SubCategory.objects.all()
        serializer = SubCategorySerializer(sub_category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'data': serializer.data
        }
        return Response(data, status=200)

    def post(self, request):
        """
        An endpoint for creating sub-category.
        """
        serializer = SubCategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors
        }
        return Response(data, status=400)

class SubCategoryDetailView(generics.GenericAPIView):
    serializer_class = SubCategorySerializer
    permission_classes = (isAdminOrReadOnly, )

    def get(self, request, sub_category_id):
        """
        An endpoint for getting sub-category detail.
        """
        sub_category_obj = SubCategory.objects.filter(id=sub_category_id)
        if sub_category_obj:
            serializer = SubCategorySerializer(sub_category_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Sub-category doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, sub_category_id):
        """
        An endpoint for updating sub-category detail.
        """
        sub_category_obj = SubCategory.objects.filter(id=sub_category_id)
        if sub_category_obj:
            serializer = SubCategorySerializer(sub_category_obj[0], data=request.data,\
                partial=True, context={'request':request})
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
                'message': "Sub-category doesn't exist."
            }
            return Response(data, status=404)

    def delete(self, request, sub_category_id):
        """
        An endpoint for deleting sub-category.
        """
        sub_category_obj = SubCategory.objects.filter(id=sub_category_id)
        if sub_category_obj:
            try:
                sub_category_obj[0].delete()
                data = {
                    'success': 1,
                    'data': None
                }
                return Response(data, status=200)
            except:
                data = {
                    'success': 0,
                    'message': 'Sub-Category cannot be deleted.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Sub-Category doesn't exist."
            }
            return Response(data, status=404)
