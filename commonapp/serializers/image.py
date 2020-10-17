from rest_framework import serializers
from commonapp.models.image import Image

class ImageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id','image', ]


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'
