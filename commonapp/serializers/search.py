from rest_framework import serializers

class TopBarSearchSerializer(serializers.Serializer):
    search_text = serializers.CharField(required = True)