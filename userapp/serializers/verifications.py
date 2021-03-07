from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from helpers.validators import phone_number_validator, is_numeric_value, otp_validator
from helpers.exceptions import (
    PhoneNumberExistsException,
    PhoneNumberNotFoundException,
    OTPCoolDownException,
    MaxResendOTPLimitReached,
    InvalidOTPException,
    InvalidTokenException,
    InvalidRequestException
)
from rest_framework.exceptions import ValidationError
from userapp.models import User, OTPVerificationCode
from helpers.choices_variable import OTP_TYPE_CHOICES
from helpers.constants import (
    MAX_LENGTHS,
    DEFAULTS,
    OTP_TYPES,
    OTP_STATUS_TYPES,
    OTP_HEADER,
    TIME_EARLY_THRESHOLD,
    RESEND_COUNTDOWN,
    OTP_VERIFY_MAX_TRIES
)
from helpers.serializer import CustomBaseSerializer
from helpers.serializer_fields import PasswordField


class SendOTPSerializer(CustomBaseSerializer):
    token = serializers.UUIDField(read_only=True)
    type = serializers.ChoiceField(choices=OTP_TYPE_CHOICES)
    phone_number_ext = serializers.CharField(
        max_length=MAX_LENGTHS['PHONE_NUMBER_EXT'],
        default=DEFAULTS['PHONE_NUMBER_EXT'],
        validators=[is_numeric_value, ],
        read_only=True
    )
    phone_number = serializers.CharField(
        max_length=MAX_LENGTHS['PHONE_NUMBER'],
        validators=[phone_number_validator, is_numeric_value]
    )
    email = serializers.EmailField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        phone_number_ext = attrs.get('phone_number_ext', DEFAULTS['PHONE_NUMBER_EXT'])
        phone_number = attrs['phone_number']
        otp_type = attrs['type']
        if otp_type == OTP_TYPES['SOCIAL_LOGIN']:
            if not 'email' in attrs:
                raise ValidationError({"Email is required."})
        try:
            self.user = User.objects.get(
                phone_number=phone_number
            )
        except User.DoesNotExist:
            if otp_type != OTP_TYPES['USER_REGISTER'] and otp_type != OTP_TYPES['SOCIAL_LOGIN']:
                raise PhoneNumberNotFoundException()
        else:
            if otp_type == OTP_TYPES['USER_REGISTER'] or otp_type == OTP_TYPES['SOCIAL_LOGIN']:
                raise PhoneNumberExistsException()

        now = timezone.now()
        one_min_earlier = now - timedelta(minutes=RESEND_COUNTDOWN)
        time_early_threshold = now - timedelta(minutes=TIME_EARLY_THRESHOLD)

        if OTPVerificationCode.objects.filter(created_at__range=[one_min_earlier, now], phone_number=phone_number, type=otp_type).exists():
            raise OTPCoolDownException()

        if OTPVerificationCode.objects.filter(created_at__range=[time_early_threshold, now], phone_number=phone_number, type=otp_type).count() > 20:
            raise MaxResendOTPLimitReached()
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        phone_number_ext = validated_data.get('phone_number_ext')
        verification_code = OTPVerificationCode.send_otp(user=self.user, **validated_data)
        return verification_code


class VerifyOTPSerializer(CustomBaseSerializer):
    """
        Verify the otp code provided along with its type for more security of random otp enter.
    """
    token = serializers.UUIDField(read_only=True)
    type = serializers.ChoiceField(choices=OTP_TYPE_CHOICES)
    code = serializers.CharField(max_length=MAX_LENGTHS['OTP'], validators=[otp_validator])
    phone_number_ext = serializers.CharField(
        max_length=MAX_LENGTHS['PHONE_NUMBER_EXT'],
        default=DEFAULTS['PHONE_NUMBER_EXT'],
        validators=[is_numeric_value, ],
        read_only=True
    )
    phone_number = serializers.CharField(
        max_length=MAX_LENGTHS['PHONE_NUMBER'],
        validators=[phone_number_validator, is_numeric_value],
        allow_null=True,
        allow_blank=True
    )
    email = serializers.EmailField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        self.otp_verification_code = None
        self.user = None
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        is_invalid = False
        tries = 0
        phone_number = attrs.get('phone_number', None)
        code = attrs.get('code', None)
        otp_type = attrs.get('type')
        if otp_type == 'SOCIAL_LOGIN':
            if not 'email' in attrs:
                raise ValidationError({"Email is required."})
        token = None
        request = self.context.get('request')
        if request:
            token = request.GET.get(OTP_HEADER)
        if not token:
            token = request.headers.get('Otp-Token')
        if not token:
            raise InvalidRequestException()
        try:
            self.user = User.objects.get(phone_number=phone_number)
        except Exception as e:
            if otp_type != OTP_TYPES['USER_REGISTER'] and otp_type != OTP_TYPES['SOCIAL_LOGIN']:
                is_invalid = True
        else:
            if otp_type == OTP_TYPES['USER_REGISTER'] or otp_type == OTP_TYPES['SOCIAL_LOGIN']:
                is_invalid = True
        if not is_invalid:
            self.otp_verification_code = OTPVerificationCode.objects.filter(
                status__in=[OTP_STATUS_TYPES['ACTIVE'], OTP_STATUS_TYPES['INACTIVE']],
                phone_number=phone_number,
                type=attrs['type'],
                code=code,
                token=token
            ).first()

            if not self.otp_verification_code:
                is_invalid = True
            else:
                tries = self.otp_verification_code.tries + 1
                code = self.otp_verification_code.code
                if attrs['code'] == code:
                    delta = timezone.now() - self.otp_verification_code.created_at
                    if delta.days >= 1:
                        is_invalid = True
                else:
                    is_invalid = True
                ## checking max tries
                max_tries = OTP_VERIFY_MAX_TRIES
                self.otp_verification_code.tries = tries
                if tries >= max_tries:
                    self.otp_verification_code.status = OTP_STATUS_TYPES['EXPIRED']
                self.otp_verification_code.save()
        if is_invalid:
            raise InvalidOTPException()
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        self.otp_verification_code.status = OTP_STATUS_TYPES['ACTIVE']
        self.otp_verification_code.save()
        return self.otp_verification_code


class VerifyOTPTokenSerializer(CustomBaseSerializer):
    token = serializers.UUIDField()

    def validate(self, attrs):
        token = attrs['token']
        if not OTPVerificationCode.objects.filter(token=token, status__in=[OTP_STATUS_TYPES['ACTIVE'], OTP_STATUS_TYPES['INACTIVE']]).exists():
            raise InvalidTokenException()
        return attrs


class SetPasswordSerializer(CustomBaseSerializer):
    password = PasswordField()
    confirm_password = PasswordField()

    def __init__(self, *args, **kwargs):
        self.otp_verification_code = None
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        if OTP_HEADER not in self.context['request'].GET:
            raise InvalidRequestException()

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"detail": "Passwords do not match"})

        try:
            self.otp_verification_code = OTPVerificationCode.objects.get(
                token=self.context['request'].GET.get(OTP_HEADER),
                status=OTP_STATUS_TYPES['ACTIVE']
            )
            delta = timezone.now() - self.otp_verification_code.created_at
            if delta.days >= 1:
                raise InvalidTokenException()

        except OTPVerificationCode.DoesNotExist:
            raise InvalidTokenException()

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.otp_verification_code.user
        user.set_password(validated_data['password'])
        self.otp_verification_code.status = OTP_STATUS_TYPES['EXPIRED']
        self.otp_verification_code.save()
        return self.otp_verification_code
