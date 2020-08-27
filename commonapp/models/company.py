# from uuid import uuid4
import shortuuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from commonapp.models.address import Address
from commonapp.models.image import Image
from commonapp.models.category import Category, SubCategory

from userapp.models import User

class Company(Address):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
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
    key = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company'
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, create key '''
        if not self.id:
            self.key = shortuuid.ShortUUID().random(length=8)
        return super(Company, self).save(*args, **kwargs)

class CompanyUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company_user'
        verbose_name_plural = 'company users'

    def __str__(self):
        return self.user.username

class FavouriteCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favourite_company'
        verbose_name_plural = "favourite companies"

    def __str__(self):
        favourite = ' loves '
        if not self.is_favourite:
            favourite = ' hates '
        return self.user.username + favourite + self.company.name