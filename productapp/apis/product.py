from django.core.paginator import Paginator
from rest_framework import generics
from rest_framework.response import Response
from company.models.company import Company, CompanyUser
from productapp.models.product import BulkQuantity, Product, ProductCategory
from productapp.serializers.product import BulkQuantitySerializer, ProductSerializer, ProductCategorySerializer
from permission import isAdminOrReadOnly, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll, publicReadOnly, isCompanySalePersonAndAllowAll
from commonapp.app_helper import custom_paginator

import code


class CompanyBulkQuantityListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BulkQuantitySerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's bulk quantities. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            # check if requesting user belongs to company
            if request.user and request.user.is_authenticated:
                company_user_obj = CompanyUser.objects.filter(user=request.user, company=company_obj[0])
            else:
                company_user_obj = False
            if company_user_obj:
                bulk_quantity_obj = BulkQuantity.objects.filter(company=company_obj[0]).order_by('-id')
                data = custom_paginator(request=request,
                                queryset=bulk_quantity_obj,
                                serializer=BulkQuantitySerializer
                            )
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "You do not have permission to view bulk quantity."
                }
                return Response(data, status=403)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist.",
            }
            return Response(data, status=404)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's bulk quantity.
        """
        if str(company_id) == str(request.data['company']):
            serializer = BulkQuantitySerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data,
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

class CompanyBulkQuantityDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = BulkQuantitySerializer

    def get(self, request, company_id, bulk_quantity_id):
        """
        An endpoint for getting vendor's bulk quantity detail.
        """
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
                        'success': 1,
                        'data': serializer.data,
                    }
                    return Response(data, status=200)
                else:
                    data = {
                        'success': 0,
                        "message": "Bulk quantity doesn't exist."
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
        """
        An endpoint for updating vendor's bulk quantity detail.
        """
        if str(company_id) == str(request.data['company']):
            company_obj = Company.objects.filter(id=company_id)
            if company_obj:
                bulk_quantity_obj = BulkQuantity.objects.filter(id=bulk_quantity_id, company=company_obj[0])
                if bulk_quantity_obj:
                    serializer = BulkQuantitySerializer(instance=bulk_quantity_obj[0],\
                        data=request.data, context={'request':request})
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
                data = {
                    'success': 0,
                    'message': "Bulk quantity doesn't exist."
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
            'message': "You do not have permission to update bulk quantity."
        }
        return Response(data, status=403)

    def delete(self, request, company_id, bulk_quantity_id):
        """
        An endpoint for deleting vendor's bulk quantity.
        """
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
                            'data': None
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


class CompanyProductListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll | isCompanySalePersonAndAllowAll | publicReadOnly]
    serializer_class = ProductSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's product. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        page_size = request.GET.get('size', 10) 
        page_number = request.GET.get('page')

        filter_fields = ['name', 'code', 'product_category', 'status']
        sort_by_fields = ['name', 'code', 'product_category', 'selling_price', 'status']

        sort_by = request.GET.get('sort_by') if request.GET.get('sort_by') in sort_by_fields else 'id'
        
        if sort_by == 'code':
            sort_by = 'product_code'
        elif sort_by == 'product_category':
            sort_by = 'product_category__name'
        order_by = '' if request.GET.get('order_by') == 'asc' else '-'

        filter_kwargs = {'{key}{lookup}'.format(
            key=key, lookup='__icontains'
            ): value for key, value in request.GET.items() if key in filter_fields}
        
        
        for item in filter_kwargs.copy():
            if filter_kwargs[item]=='':
                filter_kwargs.pop(item)

        if 'code__icontains' in filter_kwargs.keys():
            filter_kwargs['product_code'] = filter_kwargs['code__icontains']
            del filter_kwargs['code__icontains']
        
        if 'product_category__icontains' in filter_kwargs.keys():
            filter_kwargs['product_category__id__icontains'] = filter_kwargs['product_category__icontains']
            del filter_kwargs['product_category__icontains']


        product_obj = Product.objects.filter(**filter_kwargs, company=company_id).order_by(
            '{order_by}{sort_by}'.format(
                order_by=order_by,
                sort_by=sort_by
            ))

        data = custom_paginator(request=request,
                        queryset=product_obj,
                        serializer=ProductSerializer
                    )
        return Response(data, status=200)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's product.
        """
        if str(company_id) == str(request.data['company']):
            serializer = ProductSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'data': serializer.data,
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

class CompanyProductDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = ProductSerializer

    def get(self, request, company_id, product_id):
        """
        An endpoint for getting vendor's product detail.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            product_obj = Product.objects.filter(id=product_id, company=company_obj[0]).order_by('-id')
            if product_obj:
                serializer = ProductSerializer(product_obj[0], context={"request":request})
                data = {
                    'success': 1,
                    'data': serializer.data,
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    "message": "Product doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                "message" : "Company doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id, product_id):
        """
        An endpoint for updating vendor's product detail.
        """
        if str(company_id) == str(request.data['company']):
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
                            'data': serializer.data
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
        """
        An endpoint for deleting vendor's product.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            product_obj = Product.objects.filter(id=product_id, company=company_obj[0])
            if product_obj:
                try:
                    product_obj[0].delete()
                    data = {
                        'success': 1,
                        'data': None
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
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

class ProductCategoryListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = ProductCategorySerializer

    def get(self, request):
        product_category_obj = ProductCategory.objects.all()
        user = request.user
        user_id = user.id
        if user_id:
            company_user = CompanyUser.objects.select_related('company').filter(user=user_id).first()
            if company_user:
                product_category_obj = product_category_obj.filter(company=company_user.company)
        data = custom_paginator(request=request,
                        queryset=product_category_obj,
                        serializer=ProductCategorySerializer
                    )
        return Response(data, status=200)

class CompanyProductCategoryListView(generics.GenericAPIView):
    permission_classes = (isAdminOrReadOnly, )
    serializer_class = ProductCategorySerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's product categories. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            product_category_obj = ProductCategory.objects.filter(company=company_obj[0]).order_by('-id')
            data = custom_paginator(request=request,
                            queryset=product_category_obj,
                            serializer=ProductCategorySerializer
                        )
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'No product category associated with the company.'
            }
            return Response(data, status=200)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's product category.
        """
        serializer = ProductCategorySerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': serializer.errors
            }
            return Response(data, status=400)


    # def put(self, request, company_id, position_from, position_to, product_id):
    #     """
    #     An endpoint for reordering vendor's product category.
    #     """
    #     company = Company.objects.filter(id=company_id)
        
    #     serializer = ProductCategorySerializer(isinstance=)


        
    #             return Response(data, status=404)
    #     data = {
    #         'success': 0,
    #         'message': "You do not have permission to reorder product category."
    #     }
    #     return Response(data, status=403)

    
