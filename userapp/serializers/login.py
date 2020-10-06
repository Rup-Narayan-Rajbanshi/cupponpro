from rest_framework import serializers
from userapp.models.user import LoginToken

class LoginTokenSerializer(serializers.Serializer):  
    """
    Serializer for login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class LoginJWTObtainSerializer(serializers.Serializer):  
    """
    Serializer for password change endpoint.
    """
    model = LoginToken

    token = serializers.CharField(required=True)