from rest_framework import serializers
from commonapp.models.company import Company, FavouriteCompany

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"

class FavouriteCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteCompany
        fields = "__all__"