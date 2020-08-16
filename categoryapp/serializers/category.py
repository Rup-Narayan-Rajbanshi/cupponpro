from rest_framework import serializers

from categoryapp.models.category import Category, ProductCategory

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = "__all__"
