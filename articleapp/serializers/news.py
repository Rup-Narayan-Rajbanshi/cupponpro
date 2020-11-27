from rest_framework import serializers
from helpers.serializer_fields import ImageFieldWithURL
from articleapp.models.news import NewsArticle


class NewsArticleSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = NewsArticle
        fields = '__all__'

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()
