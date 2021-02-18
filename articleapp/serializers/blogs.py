from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from articleapp.models.blogs import Blog


class BlogSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Blog
        fields = '__all__'