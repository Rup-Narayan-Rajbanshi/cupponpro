from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from commonapp.models.image import Image

class ImageDetailSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Image
        fields = ['id','image', ]


class ImageSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Image
        fields = '__all__'
