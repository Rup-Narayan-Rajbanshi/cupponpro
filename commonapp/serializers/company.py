from rest_framework import serializers
from commonapp.models.company import Company, FavouriteCompany
from commonapp.serializers.image import ImageSerializer

class CompanySerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True, read_only=True)
    class Meta:
        model = Company
        fields = '__all__'

class FavouriteCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteCompany
        fields = "__all__"