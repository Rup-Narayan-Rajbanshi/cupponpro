
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

ORDER_LINE_STATUS = {
    'NEW': 'NEW',
    'START_COOKING': 'START_COOKING',
    'SERVED': 'SERVED',
    'CANCELLED': 'CANCELLED',
}

ASSET_TYPE = {
    'ROOM': 'ROOM',
    'TABLE': 'TABLE'
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
    'OTP_TYPES': OTP_TYPES['USER_REGISTER'],
    'ORDER_LINE_STATUS': ORDER_LINE_STATUS['NEW']
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

OTP_HEADER = "session"
ORDER_HEADER = "session"

COUPON_TYPE_DISPLAY_MAPPER = {
    'all': 'On all items',
    'product': 'On specific item',
    'productcategory': 'On item type'
}

COUPON_TYPE_MAPPER = {
    'product': 'product',
    'productcategory': 'productcategory',
    'all': None
}

TIME_EARLY_THRESHOLD = 30           # unit = minute
RESEND_COUNTDOWN = 1                # unit = minute
OTP_VERIFY_MAX_TRIES = 3
ORDER_SCAN_COOLDOWN = 3             # in minute
