from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.serializer import CustomModelSerializer, CustomBaseSerializer
from helpers.serializer_fields import DetailRelatedField
from commonapp.serializers.company import CompanySerializer
from helpers.constants import DISCOUNT_TYPE
from commonapp.models.company import Company, FavouriteCompany
from commonapp.models.category import Category, SubCategory
from commonapp.models.coupon import Coupon
from userapp.models import User


class FavouriteCompanySerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', read_only=True)
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation', read_only=True)


    class Meta(CustomModelSerializer.Meta):
        model = FavouriteCompany


class LocalBusinessSerializer(CompanySerializer):
    author = DetailRelatedField(model=User, lookup='id', representation='to_representation', read_only=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'logo', 'name', 'country', 'state', 'city', 'address', 'zip_code', 'author', 'images', 'discount']

    def get_discount(self, obj):
        coupon = Coupon.objects.filter(company=obj, discount_type=DISCOUNT_TYPE['PERCENTAGE']).order_by('-discount').first()
        if not coupon:
            coupon = Coupon.objects.filter(company=obj, discount_type=DISCOUNT_TYPE['FLAT']).order_by('-discount').first()
        return coupon.to_representation() if coupon else 0
