
CURRENCY_TYPES = {
    'NRS': 'NRS',
    'INR': 'INR',
    'USD': 'USD'
}

PRODUCT_STATUS_TYPE = {
    'ACTIVE': 'ACTIVE',
    'INACTIVE': 'INACTIVE'
}

ORDER_STATUS = {
    'NEW_ORDER': 'NEW_ORDER',
    'CONFIRMED': 'CONFIRMED',
    'PROCESSING': 'PROCESSING',
    'BILLABLE': 'BILLABLE',
    'CANCELLED': 'CANCELLED'
}


OTP_TYPES = {
    'USER_REGISTER': 'USER_REGISTER',
    'RESET_PASSWORD': 'RESET_PASSWORD',
    'CHANGE_PHONE_NUMBER': 'CHANGE_PHONE_NUMBER'
}

DEFAULTS = {
    'PHONE_NUMBER_EXT': '977',
    'MARITAL_STATUS': 'SINGLE',
    'CURRENCY_TYPE': CURRENCY_TYPES['NRS'],
    'PRODUCT_STATUS': PRODUCT_STATUS_TYPE['ACTIVE'],
    'ORDER_STATUS': ORDER_STATUS['NEW_ORDER'],
    'OTP_TYPES': OTP_TYPES['USER_REGISTER']
}

MAX_LENGTHS = {
    'PHONE_NUMBER_EXT': 6,
    'PHONE_NUMBER': 12,
    'ADDRESS': 200,
    'OTP': 8,
    'CURRENCY_TYPE': 4,
    'PRODUCT_STATUS': 8,
    'ORDER_STATUS': 12,
    'OTP_TYPES': 20
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

OTP_HEADER = "HTTP_OTP_TOKEN"
ORDER_HEADER = "HTTP_ORDER_TOKEN"

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

TIME_EARLY_THRESHOLD = 30           # unit = minute
RESEND_COUNTDOWN = 1                # unit = minute
OTP_VERIFY_MAX_TRIES = 3
ORDER_SCAN_COOLDOWN = 1             # in minute
