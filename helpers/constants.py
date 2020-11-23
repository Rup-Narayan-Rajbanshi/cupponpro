
CURRENCY_TYPES = {
    'NRS': 'NRS',
    'INR': 'INR',
    'USD': 'USD'
}

PRODUCT_STATUS_TYPE = {
    'ACTIVE': 'ACTIVE',
    'INACTIVE': 'INACTIVE'
}

DEFAULTS = {
    'PHONE_NUMBER_EXT': '977',
    'MARITAL_STATUS': 'SINGLE',
    'CURRENCY_TYPE': CURRENCY_TYPES['NRS'],
    'PRODUCT_STATUS': PRODUCT_STATUS_TYPE['ACTIVE']
}

MAX_LENGTHS = {
    'PHONE_NUMBER_EXT': 6,
    'PHONE_NUMBER': 14,
    'ADDRESS': 200,
    'OTP': 8,
    'CURRENCY_TYPE': 4,
    'PRODUCT_STATUS': 8
}

OTP_TYPES = {
    'USER_REGISTER': 0,
    'RESET_PASSWORD': 1,
    'CHANGE_PHONE_NUMBER': 2,
}

OTP_STATUS_TYPES = {
    'EXPIRED': 0,
    'ACTIVE': 1,
    'INACTIVE': 2
}

DISCOUNT_TYPE = {
    'FLAT': 'FLAT',
    'PERCENTAGE': 'PERCENTAGE'
}

OTP_HEADER_FOR_NEW_PASSWORD = "HTTP_NEW_PASSWORD_TOKEN"

COUPON_TYPE_DISPLAY_MAPPER = {
    'all': 'On all items',
    'product': 'On specific item',
    'category': 'On item type'
}

COUPON_TYPE_MAPPER = {
    'product': 'product',
    'category': 'category',
    'all': 'productcategory'
}
