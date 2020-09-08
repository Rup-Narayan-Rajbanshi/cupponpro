from rest_framework import serializers
from commonapp.models.image import Image

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image', ]