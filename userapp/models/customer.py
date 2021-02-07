import uuid
from django.db import models
from helpers.models import BaseModel
from helpers.validators import phone_number_validator, is_numeric_value
from helpers.constants import MAX_LENGTHS, DEFAULTS


class Customer(BaseModel):
    phone_number_ext = models.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER_EXT'],
                                        default=DEFAULTS['PHONE_NUMBER_EXT'], validators=[is_numeric_value, ])
    phone_number = models.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER'],
                                    validators=[phone_number_validator, is_numeric_value])
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=MAX_LENGTHS['EMAIL'], blank=True, default='')
    address = models.CharField(max_length=MAX_LENGTHS['ADDRESS'], default=DEFAULTS['ADDRESS'])

    @classmethod
    def get(cls, id):
        customer = cls.objects.fiter(id=id).values_list('name', 'address', 'email', 'phone_number_ext', 'phone_number', flat=True)
        data_customer = dict()
        data_customer['name'] = customer.name
        data_customer['address'] = customer.address
        data_customer['email'] = customer.email
        data_customer['phone_number_ext'] = customer.phone_number_ext
        data_customer['phone_number']  = customer.phone_number
        return data_customer