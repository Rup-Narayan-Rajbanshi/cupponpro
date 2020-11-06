from commonapp.models.salesitem import SalesItem
from rest_framework import serializers

class SalesItemSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, allow_null=True)

    class Meta:
        model = SalesItem
        fields = '__all__'