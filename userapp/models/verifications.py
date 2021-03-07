import uuid
from django.db import models
from helpers.models import BaseModel
from helpers.validators import phone_number_validator, is_numeric_value
from helpers.constants import OTP_TYPES, OTP_STATUS_TYPES, MAX_LENGTHS, DEFAULTS
from helpers.choices_variable import (
    OTP_STATUS_CHOICES,
    OTP_TYPE_CHOICES
)
from helpers.misc import make_hash_value, gen_6digit_num
from helpers.exceptions import ServerTimeOutException


class OTPVerificationCode(BaseModel):
    """
        This single model can be used for different purposes as mentioned in type field choices.
    """

    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='user_otp_verifications',
        null=True
    )
    phone_number_ext = models.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER_EXT'],
                                        default=DEFAULTS['PHONE_NUMBER_EXT'], validators=[is_numeric_value, ])
    phone_number = models.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER'],
                                    validators=[phone_number_validator, is_numeric_value])
    code = models.CharField(max_length=MAX_LENGTHS['OTP'], default=make_hash_value)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    type = models.CharField(max_length=MAX_LENGTHS['OTP_TYPES'], choices=OTP_TYPE_CHOICES, default=DEFAULTS['OTP_TYPES'])
    status = models.PositiveSmallIntegerField(choices=OTP_STATUS_CHOICES, default=OTP_STATUS_TYPES['INACTIVE'])
    tries = models.PositiveIntegerField(default=0)
    email = models.EmailField(max_length=50, null=True, blank=True)

    @staticmethod
    def generate_unique_otp_code():
        # TODO: optmize the generation by adding otp type also. So that type and code are unique at a time instead of code only.
        # for i in range(5):
        #     otp = str(gen_6digit_num())
        #
        #     if not OTPVerificationCode.objects.filter(
        #             status__in=[OTP_STATUS_TYPES['ACTIVE'], OTP_STATUS_TYPES['INACTIVE']],
        #             code=otp
        #     ).exists():
        #         break
        #
        # else:
        #     raise ServerTimeOutException()

        return '1234'

    @classmethod
    def send_otp(cls, user, **kwargs):
        from userapp.tasks import send_otp_task
        kwargs['phone_number_ext'] = kwargs.get('phone_number_ext', DEFAULTS['PHONE_NUMBER_EXT'])
        kwargs['email'] = kwargs.get('email', '')
        filter_from_kwargs = ['type', 'phone_number_ext', 'phone_number', 'email']
        assert len(set(filter_from_kwargs) - set(kwargs.keys())) == 0, "Provide all required keyword arguments."
        kwargs = {key: value for key, value in kwargs.items() if key in filter_from_kwargs}

        OTPVerificationCode.objects.filter(phone_number=kwargs['phone_number'], type=kwargs['type']).update(status=OTP_STATUS_TYPES['EXPIRED'])

        code = cls.generate_unique_otp_code()
        otp_verification_code = OTPVerificationCode.objects.create(user=user, code=code, **kwargs)
        text = 'Your code is: {}'
        # full_phone_number = "{}-{}".format(kwargs['phone_number_ext'], kwargs['phone_number'])
        text = text.format(otp_verification_code.code)
        execute = send_otp_task.delay
        execute(text=text, phone_number=kwargs['phone_number'])

        return otp_verification_code
