from rest_framework import serializers
from commonapp.models.rating import Rating

class RatingSerializer(serializers.ModelSerializer):
    company = serializers.CharField(read_only=True)
    
    class Meta:
        model = Rating
        fields = "__all__"
        write_only_fields = ('created_at',)
