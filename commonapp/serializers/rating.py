from rest_framework import serializers
from commonapp.models.rating import Rating

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = "__all__"
        write_only_fields = ('created_at',)