from django.utils import timezone
from datetime import datetime
from rest_framework.exceptions import ValidationError


def is_future_date(value):
    is_valid = True
    if isinstance(value, datetime):
        if value > timezone.now():
            is_valid = False
    else:
        if value > timezone.now().date():
            is_valid = False
    if not is_valid:
        raise ValidationError("DOB should not be future date.")

    return value


def image_validator(image):
    if image.file.size > 8 * 1024 * 512:
        raise ValidationError("Image size should be less than 1.5 MB.")
    return image


def is_numeric_value(value):
    if not value.isnumeric():
        raise ValidationError("The value should be numeric.")
    return value


def phone_number_validator(phone_no):
    if phone_no:
        if len(phone_no) != 10:
            raise ValidationError("Phone number length should be 10.")

        if phone_no[:2] != '98' :
            raise ValidationError("Phone number is invalid.")
    return phone_no


def is_alphabetic(value):
    if not value.isalpha():
        raise ValidationError("The value should be alphabetic.")
    return value


def name_validator(value):
    if value:
        if not value.replace(' ', '').replace("'", "").isalpha():
            raise ValidationError("The value should be alphabetic.")
    return value.strip()


def is_alphabetic_with_space(value):
    if not value.replace(" ", "").isalpha():
        raise ValidationError("The value should be alphabetic.")
    return value.strip()


def no_of_children_validator(value):
    if len(str(value)) > 2:
        raise ValidationError("The number of children should not be greater than 2 digits.")
    return value


def is_alphanumeric(value):
    if not value.isalnum():
        raise ValidationError("The value should be alphanumeric.")
    return value


def is_alphanumeric_with_space(value):
    if not value.replace(' ', '').isalnum():
        raise ValidationError("The value should be alphanumeric.")
    return value.strip()


def industry_risk_rate_validator(value):
    if value > 100:
        raise ValidationError("The industry risk rate should not be greater than 100")
    return value


def is_alphanumeric_with_exception(value):
    if not value.replace(' ', '').replace('-', '').isalnum():
        raise ValidationError('The value should be alphanumeric or contain only "-".')
    return value.strip()


def is_positive_numeric(value):
    is_invalid = True
    if isinstance(value, int):
        if value > 0:
            is_invalid = False
    if is_invalid:
        raise ValidationError('Value should be positive number.')
    return value
