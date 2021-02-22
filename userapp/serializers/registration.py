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
