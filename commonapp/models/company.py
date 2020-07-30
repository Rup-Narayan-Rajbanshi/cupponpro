# from uuid import uuid4
import shortuuid
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
import os
from django.utils import timezone
from commonapp.models import Address
from categoryapp.models import Category

from userapp.models import User


class Company(Address):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,\
        related_name="company_category")
    author = models.ForeignKey(User, on_delete=models.PROTECT,\
        related_name="company_author", null=True)
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

class CompanyInfo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=8)
    token_expiry_date = models.DateField()
    token_created_at = models.DateField(auto_now=True)
    discount = models.PositiveIntegerField()
    product_name = models.CharField(max_length=50,null=True,blank=True)
    price = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return self.company.name

    class Meta:
        db_table = 'companyinfo'
        verbose_name_plural = "companies info"

    def save(self, *args, **kwargs):
        ''' on save, update token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        super(CompanyInfo, self).save(*args, **kwargs)