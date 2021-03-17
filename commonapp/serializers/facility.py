from rest_framework import serializers
from company.models.facility import Facility

class FacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Facility
        fields = "__all__"