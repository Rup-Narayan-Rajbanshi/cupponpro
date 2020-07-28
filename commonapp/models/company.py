from uuid import uuid4
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
import os
from django.utils import timezone
from commonapp.models import Address
from categoryapp.models import Category


class Company(Address):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,\
        related_name="company_category")
    image = models.ImageField(upload_to='banner_image/')
    created_at = models.DateTimeField(editable=False)
    status = models.BooleanField(default=True)
    phone = models.CharField(max_length=15)
    register_number = models.CharField(_('PAN/VAT Number'), max_length=50)

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Company, self).save(*args, **kwargs)
