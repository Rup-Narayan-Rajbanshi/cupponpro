from rest_framework import serializers
from django.contrib.auth.models import Group
from userapp.models.user import User, PasswordResetToken, LoginToken, SignupToken

class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'group')

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    middle_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name',\
            'email', 'phone_number', 'active', 'admin', 'password',\
            'confirm_password', 'image', 'full_name', 'country', 'state', 'city', 'address', 'zip_code')
        read_only_fields = ('image', 'active', 'admin')

class UserDetailSerializer(serializers.ModelSerializer):
    middle_name = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    group = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name',\
            'email', 'phone_number', 'active', 'admin',\
            'image', 'full_name', 'country', 'state', 'city', 'address', 'zip_code', 'group')
        read_only_fields = ('image', 'active', 'admin', 'email')

    def get_group(self, obj):
        return obj.group.name

    def exclude_fields(self, fields_to_exclude=None):
        if isinstance(fields_to_exclude, list):
            for f in fields_to_exclude:
                f in self.fields.fields and self.fields.fields.pop(f) or next()


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    middle_name = serializers.CharField(max_length=50, required=False)
    is_user = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name',\
            'email', 'phone_number', 'password',\
            'confirm_password', 'is_user')


class CompanyUserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    middle_name = serializers.CharField(max_length=50, required=False)
    is_manager = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'last_name',\
            'email', 'phone_number', 'password',\
            'confirm_password', 'is_manager')


class ChangePasswordSerializer(serializers.Serializer):  
    """
    Serializer for password change endpoint.
    """
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetTokenSerializer(serializers.Serializer):
    """
    Serializer for password change token generation endpoint.
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

class SignupTokenSerializer(serializers.ModelSerializer):  
    """
    Serializer for signup token endpoint.
    """
    class Meta:
        model = SignupToken
        fields = '__all__'
        read_only_fields = ('is_used', )

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')

class VerifyPasswordSerializer(serializers.Serializer):  
    """
    Serializer for password verification endpoint.
    """
    model = User

    password = serializers.CharField(required=True)

class ChangeUserEmailSerializer(serializers.Serializer):  
    """
    Serializer for user's email change endpoint.
    """
    model = User

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

class ChangeUserProfilePictureSerializer(serializers.ModelSerializer):  
    """
    Serializer for user's profile picture change endpoint.
    """
    class Meta:
        model = User
        fields = ('image',)
