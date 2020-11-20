import os
import shortuuid
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from commonapp.models.address import Address
from commonapp.models.image import Image
from commonapp.models.category import Category, SubCategory
from django.dispatch import receiver
from userapp.models import User
from helpers.app_helpers import url_builder, content_file_name
from helpers.validators import image_validator


class Company(Address):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    logo_icon = models.ImageField(upload_to=content_file_name, null=True, blank=True, validators=[image_validator])
    category = models.ForeignKey(Category, on_delete=models.PROTECT,\
        related_name="company_category")
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT,\
        related_name="company_author", blank=True, null=True)
    images = GenericRelation(Image)
    status = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, \
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_affiliate = models.BooleanField(default=False)
    service_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    key = models.CharField(max_length=8)
    currency = models.CharField(max_length=10)
    invoice_counter = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company'
        verbose_name_plural = "companies"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        if self:
            logo = url_builder(self.logo, request)
            logo_icon = url_builder(self.logo_icon, request)
            return {
                'id': self.id,
                'name': self.name,
                'logo': logo,
                'logo_icon': logo_icon,
                'latitude': self.latitude,
                'longitude': self.longitude
            }
        return None

    def save(self, *args, **kwargs):
        ''' On save, create key '''
        if not self.key:
            self.key = shortuuid.ShortUUID().random(length=8)
        return super(Company, self).save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=Company)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)

@receiver(models.signals.pre_save, sender=Company)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).logo
    except:
        return False

    new_file = instance.logo
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

class CompanyUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'company_user'
        verbose_name_plural = 'company users'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.full_name

class FavouriteCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favourite_company'
        verbose_name_plural = "favourite companies"
        ordering = ['-created_at']

    def __str__(self):
        favourite = ' loves '
        if not self.is_favourite:
            favourite = ' hates '
        return self.user.full_name + favourite + self.company.name
