from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.serializer import CustomModelSerializer, CustomBaseSerializer
from helpers.serializer_fields import DetailRelatedField
from django.contrib.contenttypes.models import ContentType
from commonapp.serializers.company import CompanySerializer
from helpers.constants import DISCOUNT_TYPE
from company.models.company import Company, FavouriteCompany
from commonapp.models.category import Category, SubCategory
from productapp.models.coupon import Coupon
from userapp.models import User
from commonapp.models.image import Image
from commonapp.serializers.image import ImageDetailSerializer


class FavouriteCompanySerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', read_only=True)
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation', read_only=True)


    class Meta(CustomModelSerializer.Meta):
        model = FavouriteCompany


class LocalBusinessSerializer(CompanySerializer):
    author = DetailRelatedField(model=User, lookup='id', representation='to_representation', read_only=True)
    discount = serializers.SerializerMethodField()
    # images = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'logo', 'name', 'country', 'state', 'latitude', 'longitude',
                  'city', 'address', 'zip_code', 'author', 'images', 'discount', 'description']

    def get_discount(self, obj):
        coupon = Coupon.objects.filter(company=obj, discount_type=DISCOUNT_TYPE['PERCENTAGE']).order_by('-discount').first()
        if not coupon:
            coupon = Coupon.objects.filter(company=obj, discount_type=DISCOUNT_TYPE['FLAT']).order_by('-discount').first()
        return coupon.to_representation() if coupon else 0

    # def get_images(self,obj):
    #     image_obj = Image.objects.filter(object_id=obj.id, content_type__model='company')
    #     serializer = ImageDetailSerializer(image_obj, many=True)
    #     return serializer.data
       