from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .user import UserRegistrationSerializer
from userapp.models import User, OTPVerificationCode
from helpers.constants import OTP_STATUS_TYPES, OTP_HEADER
from helpers.exceptions import (
    InvalidRequestException
)


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
        user = User.register_user(**validated_data)
        return user
