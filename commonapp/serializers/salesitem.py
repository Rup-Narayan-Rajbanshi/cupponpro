from commonapp.models.salesitem import SalesItem
from rest_framework import serializers

class SalesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesItem
        fields = '__all__'