from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .user import UserRegistrationSerializer
from userapp.models import User, OTPVerificationCode
from helpers.constants import OTP_STATUS_TYPES, OTP_HEADER
from helpers.exceptions import (
    InvalidRequestException
)
from userapp.models.user import SocialAccount
from rest_framework.exceptions import ValidationError
from django.db import transaction
from helpers.choices_variable import ACCOUNT_TYPE_CHOICES, GENDER_CHOICES


class UserRegisterSerializer(UserRegistrationSerializer):

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        phone_number = attrs.get('phone_number')
        token = None
        request = self.context.get('request')
        if request:
            token = request.META.get(OTP_HEADER)
        if not token:
            token = request.headers.get('Otp-Token')
        if not token:
            raise InvalidRequestException()
        if password != confirm_password:
            raise ValidationError({'detail': 'The password does not match with confirm password.'})
        otp_verification_code = OTPVerificationCode.objects.filter(
                        token=token,
                        phone_number=phone_number,
                        status=OTP_STATUS_TYPES['ACTIVE']).exists()
        if not otp_verification_code:
            raise ValidationError({'detail': 'Registration token is invalid or expired.'})
        return super(UserRegisterSerializer, self).validate(attrs)

    def create(self, validated_data):
        validated_data.pop('phone_number_ext', None)
        full_name=validated_data.pop('full_name',None)
        if full_name != None:
            full_name_split= [word for word in full_name.split(" ") if word]
            first_name = full_name_split[0]
            validated_data['first_name']=first_name
            last_name_str=""
            for word in full_name_split[1:]:
                last_name_str += word + " "
            validated_data['last_name']=last_name_str
        user = User.register_user(**validated_data)
        return user

class SocialAccountSerializer(serializers.ModelSerializer):

    """
    Serializer for user's profile picture change endpoint.
    """
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    account_id = serializers.CharField(max_length=50)
    account_type = serializers.ChoiceField(ACCOUNT_TYPE_CHOICES)
    gender = serializers.ChoiceField(GENDER_CHOICES, default='M')

    class Meta:
        model = SocialAccount
        fields = ('account_id', 'is_phone_verified', 'account_type', 'first_name', 'dob', 'phone_number_ext', 'last_name', 'phone_number', 'email', 'gender')

    def validate(self, attrs):
        if 'email' in attrs:
            if User.objects.filter(email=attrs['email']).exists():
                phone = attrs['phone_number'] if 'phone_number' in attrs else None
                if User.objects.get(email=attrs['email']).phone_number != phone:
                    raise ValidationError('User with email already exists')      
        return attrs
    @transaction.atomic
    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        gender = validated_data.pop('gender')
        last_name = validated_data.pop('last_name')
        usersocial = SocialAccount.objects.filter(email=validated_data['email'], phone_number=validated_data['phone_number'])
        if usersocial.exists():
            if usersocial[0].user:
                return usersocial[0]
        user = User.objects.filter(email=validated_data['email'], phone_number=validated_data['phone_number'])
        if user.exists():
            usersocial = SocialAccount.objects.filter(user=user[0])
            if usersocial.exists():
                return usersocial
            else:
                validated_data['user'] = user[0]
                usersocial = super().create(validated_data)
                return usersocial
        usersocial = super().create(validated_data)
        if not usersocial.phone_number:
            usersocial.is_phone_verified = False
            usersocial.save()
            raise ValidationError('Phone number verification required')
        # is_phone_number_exists = User.objects.filter(phone_number = usersocial.phone_number).exists()
        # if is_phone_number_exists:
        #     usersocial.is_phone_verified = False
        #     usersocial.save()
        #     raise ValidationError('Phone number is already taken...New number is required for verification')
        data=dict()
        data['first_name'] = first_name
        data['last_name'] = last_name
        data['phone_number'] = validated_data.pop('phone_number')
        data['email'] = validated_data.pop('email')
        data['password'] = '1Xdfvd'
        data['confirm_password'] = '1Xdfvd'
        data['gender'] = gender
        data['is_user'] = True
        serializer = UserRegisterSerializer(data=data, context={'request':self.context['request']})
        if serializer.is_valid(raise_exception = True):
            usersocial.user = serializer.save()
            usersocial.user.save()
            usersocial.save()
        return usersocial
