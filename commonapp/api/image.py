from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import generics
from commonapp.models.company import Company
from commonapp.models.coupon import Coupon
from commonapp.models.image import Image
from commonapp.models.product import Product
from commonapp.serializers.image import ImageSerializer, ImageDetailSerializer
from permission import isCompanyOwnerAndAllowAll, isAdminOrReadOnly
from helper import isCompanyUser

class CompanyImageListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isAdminOrReadOnly ]
    serializer_class = ImageDetailSerializer

    def get(self, request, company_id):
        """
        An endpoint for listing all the vendor's image.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            image_obj = Image.objects.filter(object_id=company_obj[0].id, content_type=ContentType.objects.get(model='company').id)
            serializer = ImageDetailSerializer(image_obj, many=True, context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

    def post(self, request, company_id):
        """
        An endpoint for creating vendor's image.
        """
        if isCompanyUser(request.user.id, company_id):
            request_data = request.data
            request_data['object_id'] = company_id
            request_data['content_type'] = ContentType.objects.get(model='company').id
            serializer = ImageSerializer(data=request_data, context={'request':request})
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
                'message': "You don't have permission to add company image."
            }
            return Response(data, status=403)

class CompanyImageDetailView(generics.GenericAPIView):
    permission_classes = (isCompanyOwnerAndAllowAll, )
    serializer_class = ImageDetailSerializer

    def get(self, request, company_id, image_id):
        """
        An endpoint for getting vendor's image detail.
        """
        image_obj = Image.objects.filter(id=image_id, object_id=company_id, content_type=ContentType.objects.get(model='company').id)
        if image_obj:
            serializer = ImageDetailSerializer(image_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Image doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, company_id, image_id):
        """
        An endpoint for updating vendor's image detail.
        """
        if isCompanyUser(request.user.id, company_id):
            image_obj = Image.objects.filter(id=image_id, object_id=company_id, content_type=ContentType.objects.get(model='company').id)
            if image_obj:
                serializer = ImageDetailSerializer(instance=image_obj[0], data=request.data, context={'request':request})
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
                    'message': "Image doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to modify company image."
            }
            return Response(data, status=403)

    def delete(self, request, company_id, image_id):
        """
        An endpoint for deleting vendor's image.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            image_obj = Image.objects.filter(id=image_id, object_id=company_id, content_type=ContentType.objects.get(model='company').id)
            if image_obj:
                try:
                    image_obj[0].delete()
                    data = {
                        'success': 1,
                        'data': None
                    }
                    return Response(data, status=200)
                except:
                    data = {
                        'success': 0,
                        'message': "Image cannot be deleted."
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "Image doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                'message' : "Company doesn't exist.",
            }
            return Response(data, status=404)

class CouponImageListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isAdminOrReadOnly ]
    serializer_class = ImageDetailSerializer

    def get(self, request, coupon_id):
        """
        An endpoint for listing all the coupon's image.
        """
        coupon_obj = Coupon.objects.filter(id=coupon_id)
        if coupon_obj:
            image_obj = Image.objects.filter(object_id=coupon_obj[0].id, content_type=ContentType.objects.get(model='coupon').id)
            serializer = ImageDetailSerializer(image_obj, many=True, context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Coupon doesn't exist."
            }
            return Response(data, status=404)

    def post(self, request, coupon_id):
        """
        An endpoint for creating coupon's image.
        """
        if isCompanyUser(request.user.id, coupon_id):
            request_data = request.data
            request_data['object_id'] = coupon_id
            request_data['content_type'] = ContentType.objects.get(model='coupon').id
            serializer = ImageSerializer(data=request_data, context={'request':request})
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
                'message': "You don't have permission to add coupon image."
            }
            return Response(data, status=403)

class CouponImageDetailView(generics.GenericAPIView):
    permission_classes = (isCompanyOwnerAndAllowAll, )
    serializer_class = ImageDetailSerializer

    def get(self, request, coupon_id, image_id):
        """
        An endpoint for getting coupon's image detail.
        """
        image_obj = Image.objects.filter(id=image_id, object_id=coupon_id, content_type=ContentType.objects.get(model='coupon').id)
        if image_obj:
            serializer = ImageDetailSerializer(image_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Image doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, coupon_id, image_id):
        """
        An endpoint for updating coupon's image detail.
        """
        if isCompanyUser(request.user.id, coupon_id):
            image_obj = Image.objects.filter(id=image_id, object_id=coupon_id, content_type=ContentType.objects.get(model='coupon').id)
            if image_obj:
                serializer = ImageDetailSerializer(instance=image_obj[0], data=request.data, context={'request':request})
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
                    'message': "Image doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to modify coupon image."
            }
            return Response(data, status=403)

    def delete(self, request, coupon_id, image_id):
        """
        An endpoint for deleting coupon's image.
        """
        coupon_obj = Coupon.objects.filter(id=coupon_id)
        if coupon_obj:
            image_obj = Image.objects.filter(id=image_id, object_id=coupon_id, content_type=ContentType.objects.get(model='coupon').id)
            if image_obj:
                try:
                    image_obj[0].delete()
                    data = {
                        'success': 1,
                        'data': None
                    }
                    return Response(data, status=200)
                except:
                    data = {
                        'success': 0,
                        'message': "Image cannot be deleted."
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "Image doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                'message' : "Coupon doesn't exist.",
            }
            return Response(data, status=404)

class ProductImageListView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isAdminOrReadOnly ]
    serializer_class = ImageDetailSerializer

    def get(self, request, product_id):
        """
        An endpoint for listing all the product's image.
        """
        product_obj = Product.objects.filter(id=product_id)
        if product_obj:
            image_obj = Image.objects.filter(object_id=product_obj[0].id, content_type=ContentType.objects.get(model='product').id)
            serializer = ImageDetailSerializer(image_obj, many=True, context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Product doesn't exist."
            }
            return Response(data, status=404)

    def post(self, request, product_id):
        """
        An endpoint for creating product's image.
        """
        if isCompanyUser(request.user.id, product_id):
            request_data = request.data
            request_data['object_id'] = product_id
            request_data['content_type'] = ContentType.objects.get(model='product').id
            serializer = ImageSerializer(data=request_data, context={'request':request})
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
                'message': "You don't have permission to add product image."
            }
            return Response(data, status=403)

class ProductImageDetailView(generics.GenericAPIView):
    permission_classes = (isCompanyOwnerAndAllowAll, )
    serializer_class = ImageDetailSerializer

    def get(self, request, product_id, image_id):
        """
        An endpoint for getting product's image detail.
        """
        image_obj = Image.objects.filter(id=image_id, object_id=product_id, content_type=ContentType.objects.get(model='product').id)
        if image_obj:
            serializer = ImageDetailSerializer(image_obj[0], context={'request':request})
            data = {
                'success': 1,
                'data': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Image doesn't exist."
            }
            return Response(data, status=404)

    def put(self, request, product_id, image_id):
        """
        An endpoint for updating product's image detail.
        """
        if isCompanyUser(request.user.id, product_id):
            image_obj = Image.objects.filter(id=image_id, object_id=product_id, content_type=ContentType.objects.get(model='product').id)
            if image_obj:
                serializer = ImageDetailSerializer(instance=image_obj[0], data=request.data, context={'request':request})
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
                    'message': "Image doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to modify product image."
            }
            return Response(data, status=403)

    def delete(self, request, product_id, image_id):
        """
        An endpoint for deleting product's image.
        """
        product_obj = Coupon.objects.filter(id=product_id)
        if product_obj:
            image_obj = Image.objects.filter(id=image_id, object_id=product_id, content_type=ContentType.objects.get(model='product').id)
            if image_obj:
                try:
                    image_obj[0].delete()
                    data = {
                        'success': 1,
                        'data': None
                    }
                    return Response(data, status=200)
                except:
                    data = {
                        'success': 0,
                        'message': "Image cannot be deleted."
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "Image doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success' : 0,
                'message' : "Coupon doesn't exist.",
            }
            return Response(data, status=404)
