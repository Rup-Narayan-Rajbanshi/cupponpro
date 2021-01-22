from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from commonapp.serializers.company import CompanySerializer
from helpers.serializer_fields import ImageFieldWithURL
from company.models import Partner


class PartnerSerializer(CustomModelSerializer):
    logo = ImageFieldWithURL()

    class Meta(CustomModelSerializer.Meta):
        model = Partner
