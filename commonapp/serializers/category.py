from rest_framework import serializers
from commonapp.models.category import Category, SubCategory
from helpers.serializer_fields import ImageFieldWithURL, FileFieldWithURL


class CategorySerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=True)
    icon = ImageFieldWithURL(allow_empty_file=False)

    class Meta:
        model = Category
        exclude = ('token', )

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = "__all__"
