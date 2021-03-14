from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from company.models.advertisement import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Advertisement
        fields = '__all__'