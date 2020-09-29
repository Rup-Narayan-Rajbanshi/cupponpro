from rest_framework import serializers

class LoginJWTTokenSerializer(serializers.Serializer):  
    """
    Serializer for login JWT token.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    group = serializers.CharField(required=True)