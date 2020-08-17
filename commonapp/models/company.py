# from uuid import uuid4
import shortuuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from commonapp.models.address import Address
from commonapp.models.image import Image
from categoryapp.models import Category, SubCategory

from userapp.models import User

class Company(Address):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,\
        related_name="company_category")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT,\
        related_name="company_author", null=True)
    images = GenericRelation(Image)
    status = models.BooleanField(default=True)
    phone = models.CharField(max_length=15)
    register_number = models.CharField(_('PAN/VAT Number'), max_length=50)
    is_partner = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company'
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.key = shortuuid.ShortUUID().random(length=8)
        return super(Company, self).save(*args, **kwargs)

class FavouriteCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'favouritecompany'
        verbose_name_plural = "favourite companies"

    def __str__(self):
        return self.user.username + ' loves ' + self.company.name