from bannerapp.models.banner import Banner
from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL


class BannerSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Banner
        fields = '__all__'

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()
