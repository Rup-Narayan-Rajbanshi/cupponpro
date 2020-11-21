from .constants import DISCOUNT_TYPE, OTP_STATUS_TYPES, OTP_TYPES


DISCOUNT_CHOICES = (
    (DISCOUNT_TYPE['FLAT'], 'Flat'),
    (DISCOUNT_TYPE['PERCENTAGE'], 'Percentage')
)

OTP_STATUS_CHOICES = (
    (OTP_STATUS_TYPES['EXPIRED'], 'Expired'),
    (OTP_STATUS_TYPES['ACTIVE'], 'Active'),
    (OTP_STATUS_TYPES['INACTIVE'], 'Inactive')
)

OTP_TYPE_CHOICES = (
    (OTP_TYPES['USER_REGISTER'], 'User Registration'),
    (OTP_TYPES['RESET_PASSWORD'], 'Reset Password'),
    (OTP_TYPES['CHANGE_PHONE_NUMBER'], 'Change Phone number')
)
