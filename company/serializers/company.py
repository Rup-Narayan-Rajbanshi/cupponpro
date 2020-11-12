from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.serializer import CustomModelSerializer, CustomBaseSerializer
from helpers.serializer_fields import DetailRelatedField
from commonapp.models.company import Company, FavouriteCompany
from userapp.models import User

class FavouriteCompanySerializer(CustomModelSerializer):
    company = DetailRelatedField(model=User, lookup='idx', representation='to_representation', read_only=True)
    user = DetailRelatedField(model=User, lookup='idx', representation='to_representation', read_only=True)

    class Meta(CustomModelSerializer.Meta):
        model = FavouriteCompany
