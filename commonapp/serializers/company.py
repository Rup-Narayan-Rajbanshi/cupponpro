from rest_framework import serializers
from commonapp.models.company import Company

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = "__all__"