from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from company.models.advertisement import Advertisement
from helpers.serializer import CustomModelSerializer


class AdvertisementSerializer(CustomModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Advertisement
        fields = '__all__'