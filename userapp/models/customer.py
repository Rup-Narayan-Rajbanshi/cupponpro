import uuid
from django.db import models
from helpers.models import BaseModel
from helpers.validators import phone_number_validator, is_numeric_value
from helpers.constants import MAX_LENGTHS, DEFAULTS


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
        required_data = ['phone_number', 'name']
        assert(set(required_data).issubset(kwargs)),'Phone number and name is both required'
        optional_data = ['email', 'address','phone_number_ext']
        data_list = required_data + optional_data
        valid_data = dict()
        for data in data_list:
            if data in kwargs:
                valid_data[data] = kwargs.get(data)
        cusotmer = None
        phone_number = kwargs.get('phone_number')
        try:
            customer = cls.objects.get(phone_number=phone_number)
        except:
            customer = Customer.objects.create(valid_data)
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