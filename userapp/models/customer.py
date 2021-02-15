import uuid
from django.db import models
from helpers.models import BaseModel
from helpers.validators import phone_number_validator, is_numeric_value
from helpers.constants import MAX_LENGTHS, DEFAULTS
from rest_framework.exceptions import ValidationError


class Customer(BaseModel):
    phone_number_ext = models.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER_EXT'],
                                        default=DEFAULTS['PHONE_NUMBER_EXT'], validators=[is_numeric_value, ])
    phone_number = models.CharField(max_length=MAX_LENGTHS['PHONE_NUMBER'],
                                    validators=[phone_number_validator, is_numeric_value], unique=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=MAX_LENGTHS['EMAIL'], blank=True, default='')
    address = models.CharField(max_length=MAX_LENGTHS['ADDRESS'], default=DEFAULTS['ADDRESS'])

    @classmethod
    def getcreate_customer(cls, **kwargs):
        customer = None
        phone_number = kwargs.get('phone_number')
        name = kwargs.get('name')
        if phone_number:
            # optional_data = ['email', 'address','phone_number_ext']
            # data_list = required_data + optional_data
            # valid_data = dict()
            # for data in data_list:
            #     if data in kwargs:
            #         valid_data[data] = kwargs.get(data)
            try:
                customer = cls.objects.get(phone_number=phone_number)
            except:
                name = kwargs.get('name')
                if name == '':
                    raise ValidationError({'detail':'Phone number and name is both required to create customer.'})
                customer = cls.objects.create(**kwargs)
        else:
            raise ValidationError({'detail':'Phone number and name is both required to create customer.'})
        return customer

    def to_representation(self, request=None):
        if self:
            return {
                "id": self.id,
                "phone_number_ext": self.phone_number_ext,
                "phone_number": self.phone_number,
                "name": self.name,
                "email": self.email,
                "address": self.address
            }
        return None
