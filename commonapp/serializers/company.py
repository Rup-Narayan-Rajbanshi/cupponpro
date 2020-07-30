from rest_framework import serializers
from commonapp.models.company import Company, CompanyInfo

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"

class CompanyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyInfo
        fields = "__all__" 