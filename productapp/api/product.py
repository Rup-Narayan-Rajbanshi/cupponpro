from rest_framework.views import APIView
from rest_framework.response import Response
from productapp.serializers.product import BulkQuantitySerializer, ProductSerializer, ProductCategorySerializer
from commonapp.models.company import Company
from productapp.models.product import BulkQuantity, Product, ProductCategory
from permission import isAdminOrReadOnly, isCompanyOwner, isCompanyManager

class BulkQuantityListView(APIView):
    permission_classes = (isCompanyOwner, isCompanyManager)
    serializer_class = BulkQuantitySerializer

    def get(self, request):
        bulk_quantity_obj = BulkQuantity.objects.all()
        serializer = BulkQuantitySerializer(bulk_quantity_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'bulkquantity' : serializer.data,
        }
        return Response(data, status=200)

    def post(self, request):
        if request.user.admin:
            serializer = BulkQuantitySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'bulkquantity': serializer.data,
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors,
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to add a bulk quantity."
        }
        return Response(data, status=403)

class BulkQuantityDetailView(APIView):
    permission_classes = (isCompanyOwner, isCompanyManager)
    serializer_class = BulkQuantitySerializer

    def get(self, request, bulk_quantity_id):
        if BulkQuantity.objects.filter(id=bulk_quantity_id):
            bulk_quantity_obj = BulkQuantity.objects.get(id=bulk_quantity_id)
            serializer = BulkQuantitySerializer(bulk_quantity_obj, \
                context={"request":request})
            data = {
                'success' : 1,
                'bulkquantity' : serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success' : 0,
                "message" : "Bulkquantity id not found."
            }
            return Response(data, status=404)

    def put(self, request, bulk_quantity_id):
        if request.user.admin:
            if BulkQuantity.objects.filter(id=bulk_quantity_id):
                bulk_quantity_obj = BulkQuantity.objects.get(id=bulk_quantity_id)
                serializer = BulkQuantitySerializer(instance=bulk_quantity_obj,\
                    data=request.data, context={'request':request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'bulkquantity': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': "Bulkquantity id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to update bulkquantity."
        }
        return Response(data, status=403)

    def delete(self, request, bulk_quantity_id):
        if request.user.admin:
            if BulkQuantity.objects.filter(id=bulk_quantity_id):
                bulk_quantity_obj = BulkQuantity.objects.get(id=bulk_quantity_id)
                bulk_quantity_obj.delete()
                data = {
                    'success': 1,
                    'bulkquantity': "Bulkquantity deleted successfully."
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': "Bulkquantity id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to delete Bulkquantity."
        }
        return Response(data, status=403)

class ProductListView(APIView):
    permission_classes = (isCompanyOwner, isCompanyManager)
    serializer_class = ProductSerializer

    def get(self, request):
        product_obj = Product.objects.all()
        serializer = ProductSerializer(product_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'product' : serializer.data,
        }
        return Response(data, status=200)

    def post(self, request):
        if request.user.admin:
            serializer = ProductSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'product': serializer.data,
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors,
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to add a product."
        }
        return Response(data, status=403)

class ProductDetailView(APIView):
    permission_classes = (isCompanyOwner, isCompanyManager)
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        if Product.objects.filter(id=product_id):
            product_obj = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product_obj, \
                context={"request":request})
            data = {
                'success' : 1,
                'product' : serializer.data,
            }
            return Response(data, status=200)
        else:
            data = {
                'success' : 0,
                "message" : "Product id not found."
            }
            return Response(data, status=404)

    def put(self, request, product_id):
        if request.user.admin:
            if Product.objects.filter(id=product_id):
                product_obj = Product.objects.get(id=product_id)
                serializer = ProductSerializer(instance=product_obj,\
                    data=request.data, context={'request':request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'product': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': "Product id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to update product."
        }
        return Response(data, status=403)

    def delete(self, request, product_id):
        if request.user.admin:
            if Product.objects.filter(id=product_id):
                product_obj = Product.objects.get(id=product_id)
                product_obj.delete()
                data = {
                    'success': 1,
                    'product': "Product deleted successfully."
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': "Product id not found."
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': "You do not have permission to delete product."
        }
        return Response(data, status=403)

class ProductCategoryListView(APIView):
    permission_classes = (isAdminOrReadOnly ,)
    serializer_class = ProductCategorySerializer

    def get(self, request):
        product_category_obj = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(product_category_obj, many=True,\
        context={"request": request})
        data = {
            'success': 1,
            'product_category': serializer.data
        }
        return Response(data, status=200)

class CompanyProductCategoryListView(APIView):
    permission_classes = (isAdminOrReadOnly ,)
    serializer_class = ProductCategorySerializer

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_obj)
        if company_obj:
            product_category_obj = ProductCategory.objects.filter(company = company_obj[0])
            serializer = ProductCategorySerializer(product_category_obj, many=True,\
            context={"request": request})
            data = {
                'success': 1,
                'product_category': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'No product category associated with the company.'
            }
            return Response(data, status=200)


    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'product_category': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': serializer.errors
            }
            return Response(data, status=400)