from rest_framework.views import APIView
from rest_framework.response import Response
from commonapp.models.company import Company, CompanyUser
from productapp.models.product import BulkQuantity, Product, ProductCategory
from productapp.serializers.product import BulkQuantitySerializer, ProductSerializer, ProductCategorySerializer
from permission import isAdminOrReadOnly, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll

class CompanyBulkQuantityListView(APIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BulkQuantitySerializer

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            # check if requesting user belongs to company
            if request.user and request.user.is_authenticated:
                company_user_obj = CompanyUser.objects.filter(user=request.user, company=company_obj[0])
            else:
                company_user_obj = False
            if company_user_obj:
                bulk_quantity_obj = BulkQuantity.objects.filter(company=company_obj[0])
                serializer = BulkQuantitySerializer(bulk_quantity_obj, many=True,\
                    context={"request":request})
                data = {
                    'success' : 1,
                    'bulk_quantity' : serializer.data,
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "You do not have permission to view bulk quantity."
                }
                return Response(data, status=403)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

    def post(self, request, company_id):
        if company_id == int(request.data['company']):
            serializer = BulkQuantitySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'bulk_quantity': serializer.data,
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors,
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "You do not have permission to add a bulk quantity of other company."
            }
            return Response(data, status=403)

class CompanyBulkQuantityDetailView(APIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BulkQuantitySerializer

    def get(self, request, company_id, bulk_quantity_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            if request.user and request.user.is_authenticated:
                company_user_obj = CompanyUser.objects.filter(user=request.user, company=company_obj[0])
            else:
                company_user_obj = False
            if company_user_obj:
                bulk_quantity_obj = BulkQuantity.objects.filter(id=bulk_quantity_id)
                if bulk_quantity_obj:
                    serializer = BulkQuantitySerializer(bulk_quantity_obj[0], \
                        context={"request":request})
                    data = {
                        'success' : 1,
                        'bulk_quantity' : serializer.data,
                    }
                    return Response(data, status=200)
                else:
                    data = {
                        'success' : 0,
                        "message" : "Bulk quantity doesn't exist."
                    }
                    return Response(data, status=404)
            else:
                data = {
                    'success': 0,
                    'message': "You do not have permission to view bulk quantity."
                }
                return Response(data, status=403)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

    def put(self, request, company_id, bulk_quantity_id):
        if company_id == int(request.data['company']):
            bulk_quantity_obj = BulkQuantity.objects.filter(id=bulk_quantity_id)
            if bulk_quantity_obj:
                serializer = BulkQuantitySerializer(instance=bulk_quantity_obj[0],\
                    data=request.data, context={'request':request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'bulk_quantity': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': "Bulk quantity doesn't exist."
            }
            return Response(data, status=404)
        data = {
            'success': 0,
            'message': "You do not have permission to update bulk quantity."
        }
        return Response(data, status=403)

    def delete(self, request, company_id, bulk_quantity_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            if request.user and request.user.is_authenticated:
                company_user_obj = CompanyUser.objects.filter(user=request.user, company=company_obj[0])
            else:
                company_user_obj = False
            if company_user_obj:
                bulk_quantity_obj = BulkQuantity.objects.filter(id=bulk_quantity_id)
                if bulk_quantity_obj:
                    try:
                        bulk_quantity_obj[0].delete()
                        data = {
                            'success': 1,
                            'bulk_quantity': "Bulk quantity deleted successfully."
                        }
                        return Response(data, status=200)
                    except:
                        data = {
                            'success': 0,
                            'message': "Bulk quantity cannot be deleted."
                        }
                        return Response(data, status=400)
                data = {
                    'success': 0,
                    'message': "Bulk quantity doesn't exist."
                }
                return Response(data, status=404)
            else:
                data = {
                    'success': 0,
                    'message': "You do not have permission to delete Bulkquantity."
                }
                return Response(data, status=403)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

class CompanyProductListView(APIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = ProductSerializer

    def get(self, request, company_id):
        product_obj = Product.objects.filter(company=company_id)
        serializer = ProductSerializer(product_obj, many=True,\
            context={"request":request})
        data = {
            'success' : 1,
            'product' : serializer.data,
        }
        return Response(data, status=200)

    def post(self, request, company_id):
        if company_id == int(request.data['company']):
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

class CompanyProductDetailView(APIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = ProductSerializer

    def get(self, request, company_id, product_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            product_obj = Product.objects.filter(id=product_id, company=company_obj[0])
            if product_obj:
                serializer = ProductSerializer(product_obj[0], context={"request":request})
                data = {
                    'success' : 1,
                    'product' : serializer.data,
                }
                return Response(data, status=200)
            else:
                data = {
                    'success' : 0,
                    "message" : "Product doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                "message" : "Company doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id, product_id):
        if company_id == int(request.data['company']):
            company_obj = Company.objects.filter(id=company_id)
            if company_obj:
                product_obj = Product.objects.filter(id=product_id, company=company_obj[0])
                if product_obj:
                    serializer = ProductSerializer(instance=product_obj[0],\
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
                    'message': "Product doesn't exist."
                }
                return Response(data, status=404)
            else:
                data = {
                    'success': 0,
                    'message': "Company doesn't exist."
                }
                return Response(data, status=404)
        data = {
            'success': 0,
            'message': "You do not have permission to update product."
        }
        return Response(data, status=403)

    def delete(self, request, company_id, product_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            product_obj = Product.objects.filter(id=product_id, company=company_obj[0])
            if product_obj:
                try:
                    product_obj[0].delete()
                    data = {
                        'success': 1,
                        'product': "Product deleted successfully."
                    }
                    return Response(data, status=200)
                except:
                    data = {
                        'success': 0,
                        'message': "Product cannot be deleted."
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "Product doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "COmpany doesn't exist."
            }
            return Response(data, status=404)

class ProductCategoryListView(APIView):
    permission_classes = (isAdminOrReadOnly, )
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
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = ProductCategorySerializer

    def get(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            product_category_obj = ProductCategory.objects.filter(company=company_obj[0])
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
            