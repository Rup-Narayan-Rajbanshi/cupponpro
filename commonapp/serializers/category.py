from rest_framework import serializers

from commonapp.models.category import Category, SubCategory

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('token', )

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = "__all__"
