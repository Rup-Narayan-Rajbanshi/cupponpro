from userapp.models.user import User, PasswordResetToken
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    middle_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name',\
            'username', 'email', 'phone_number', 'active', 'admin', 'password',\
            'confirm_password', 'image', 'full_name',)
        read_only_fields = ('image', 'active', 'admin')

class UserDetailSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name',\
            'username', 'email', 'phone_number', 'active', 'admin',\
            'image', 'full_name',)
        read_only_fields = ('image', 'active', 'admin')

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetTokenSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    model = PasswordResetToken

    email = serializers.EmailField(max_length=50)

    def create(self, validated_data):
        user = User.objects.get(email=validated_data.get('email'))
        return PasswordResetToken.objects.create(user=user)    

class ResetPasswordSerializer(serializers.Serializer):  
    """
    Serializer for password change endpoint.
    """
    model = User

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# class UpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'middle_name', 'last_name',\
#             'phone_number', 'email', 'group', 'active', 'admin', 'password',\
#             'confirm_password', 'image')
#         read_only_fields = ('image', 'active')
