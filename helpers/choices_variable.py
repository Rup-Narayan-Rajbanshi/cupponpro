from .constants import (
    DISCOUNT_TYPE,
    OTP_STATUS_TYPES,
    OTP_TYPES,
    CURRENCY_TYPES,
    PRODUCT_STATUS_TYPE,
    ORDER_STATUS
)


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

CURRENCY_TYPE_CHOICES = (
    (CURRENCY_TYPES['NRS'], 'NRS'),
    (CURRENCY_TYPES['INR'], 'INR'),
    (CURRENCY_TYPES['USD'], 'USD')
)

PRODUCT_STATUS_CHOICES = (
    (PRODUCT_STATUS_TYPE['ACTIVE'], 'Active'),
    (PRODUCT_STATUS_TYPE['INACTIVE'], 'Inactive')
)

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS['NEW_ORDER'], 'New Order'),
    (ORDER_STATUS['CONFIRMED'], 'Confirmed'),
    (ORDER_STATUS['PROCESSING'], 'Processing'),
    (ORDER_STATUS['BILLABLE'], 'Billable'),
    (ORDER_STATUS['CANCELLED'], 'Cancelled')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)
