from uuid import uuid4
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
import os
from django.utils import timezone






class Address(models.Model):
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)

    class Meta:
        db_table = 'address'
        abstract = True
