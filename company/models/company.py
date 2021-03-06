import os
import shortuuid
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from commonapp.models.address import Address
from commonapp.models.image import Image
from commonapp.models.category import Category, SubCategory
from django.dispatch import receiver
from userapp.models import User
from helpers.app_helpers import url_builder, content_file_name
from helpers.validators import image_validator
from helpers.models import BaseModel


class Company(Address):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    logo_icon = models.ImageField(upload_to=content_file_name, null=True, blank=True)
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
    description = models.TextField(blank=True, null=True)
    pan_number  = models.CharField(max_length=16, default='')
    print_tax_invoice = models.BooleanField(default=True)
    print_pre_order_bill = models.BooleanField(default=False)
    print_order = models.BooleanField(default=True)
    #affiliate addition
    url = models.TextField(null=True, blank=True)
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    deal_of_the_day = models.BooleanField(default=False)

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
                'longitude': self.longitude,
                'pan_number': self.pan_number,
                'phone_number': self.phone_number,
                'print_tax_invoice' : self.print_tax_invoice,
                'print_pre_order_bill' : self.print_pre_order_bill,
                'print_order' : self.print_order,
                'service_charge': self.service_charge,
                'is_affiliate': self.is_affiliate
            }
        return None


    def inventory_representation(self, request=None):
        if self:
            logo = url_builder(self.logo, request)
            logo_icon = url_builder(self.logo_icon, request)
            return {
                'id': self.id,
                'name': self.name,
            }
        return None

    def save(self, *args, **kwargs):
        ''' On save, create key '''
        if not self.key:
            self.key = shortuuid.ShortUUID().random(length=8)
        return super(Company, self).save(*args, **kwargs)

    def get_or_create_company_customer_user(self):
        pass

    @property
    @transaction.atomic
    def qr_user(self):
        category = Category.objects.filter(name__icontains='Rest', ).first()
        company_user = CompanyUser.objects.filter(is_qr_user=True).first()
        if company_user:
            return company_user.user
        else:
            user, is_created = User.objects.get_or_create(
                first_name=self.name,
                last_name=category.name)
            CompanyUser.objects.get_or_create(user=user, company=self, is_qr_user=True, is_staff=False)
            return user


@receiver(models.signals.post_delete, sender=Company)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)

    if instance.logo_icon:
        if os.path.isfile(instance.logo_icon.path):
            os.remove(instance.logo_icon.path)
    

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
        old_instance = sender.objects.get(pk=instance.pk)
    except:
        return False
    old_file = old_instance.logo
    old_logo_icon = old_instance.logo_icon
    new_file = instance.logo
    new_logo_icon = instance.logo_icon
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    if old_logo_icon:
        if not old_logo_icon == new_logo_icon:
            if os.path.isfile(old_logo_icon.path):
                os.remove(old_logo_icon.path)


class CompanyUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='company_user')
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=True)
    is_obsolete = models.BooleanField(default=False)
    is_qr_user = models.BooleanField(default=False)

    class Meta:
        db_table = 'company_user'
        verbose_name_plural = 'company users'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.full_name

    # @classmethod
    # def get_or_create_customer_user(self):
    #     Group.ob


class FavouriteCompany(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)

    class Meta:
        db_table = 'favourite_company'
        verbose_name_plural = "favourite companies"
        ordering = ['-created_at']

    def __str__(self):
        favourite = ' loves '
        if not self.is_favourite:
            favourite = ' hates '
        return self.user.full_name + favourite + self.company.name
