import os
import shortuuid
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

from commonapp.models.image import Image
from company.models.company import Company
from helpers.app_helpers import url_builder, content_file_name
from helpers.constants import DEFAULTS, MAX_LENGTHS, DISCOUNT_TYPE
from helpers.choices_variable import CURRENCY_TYPE_CHOICES, PRODUCT_STATUS_CHOICES, PRODUCT_CAT_TYPE_CHOICES, PRODUCT_TYPE_CHOICES
from helpers.models import BaseModel


class BulkQuantity(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'bulk_quantity'
        verbose_name_plural = "bulk quantities"

    def __str__(self):
        return self.name


class ProductCategory(BaseModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategory', null=True)
    name = models.CharField(max_length=64)
    link = models.URLField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=content_file_name)
    token = models.CharField(max_length=8, editable=False)
    types = models.CharField(max_length=MAX_LENGTHS['PRODUCT_CAT_TYPE'], choices=PRODUCT_CAT_TYPE_CHOICES, default=DEFAULTS['PRODUCT_CAT_TYPE'])
    sub_type = models.CharField(max_length=MAX_LENGTHS['PRODUCT_CAT_SUB_TYPE'], default=DEFAULTS['PRODUCT_CAT_SUB_TYPE'], null=True)
    position = models.PositiveIntegerField(default=0, blank=True)

    
    class Meta:
        db_table = 'product_category'
        verbose_name_plural = "product categories"
        unique_together = ('name', 'company')

    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        image = url_builder(self.image, request)
        return {
            "id": self.id,
            "name": self.name,
            "image": image,
            "link": self.link,
            'parent': self.parent.to_representation() if self.parent else None,
            'types': self.types,
            'sub_type': self.sub_type if self.sub_type else ''
        }

    def to_represent_minimal(self, request=None):
        return self.to_representation(request=request)

    def save(self, *args, **kwargs):
        ''' On save, create token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        return super(ProductCategory, self).save(*args, **kwargs)

@receiver(models.signals.post_delete, sender=ProductCategory)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=ProductCategory)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except:
        return False

    new_file = instance.image
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)


class Product(BaseModel):
    # Null = None
    # Male = "M"
    # Female = "F"
    # Unisex = "U"
    # GENDER = [
    #     (Null, ''),
    #     (Male, 'Male'),
    #     (Female, 'Female'),
    #     (Unisex, 'Unisex'),
    # ]
    product_code = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    link = models.URLField(null=True, blank=True)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=30, null=True, blank=True)
    purchase_price = models.PositiveIntegerField(default=0)
    purchase_currency = models.CharField(max_length=MAX_LENGTHS['CURRENCY_TYPE'], choices=CURRENCY_TYPE_CHOICES, default=DEFAULTS['CURRENCY_TYPE'])
    selling_price = models.PositiveIntegerField()
    selling_currency = models.CharField(max_length=MAX_LENGTHS['CURRENCY_TYPE'], choices=CURRENCY_TYPE_CHOICES, default=DEFAULTS['CURRENCY_TYPE'])
    bulk_quantity = models.ForeignKey(BulkQuantity, on_delete=models.PROTECT, null=True, blank=True)
    total_price = models.PositiveIntegerField(blank=True, null=True)
    token = models.CharField(max_length=8, editable=False)
    types = models.CharField(max_length=MAX_LENGTHS['PRODUCT_TYPE'], choices=PRODUCT_TYPE_CHOICES, default=DEFAULTS['PRODUCT_TYPE'], null=True)
    #only for food item
    # gender = models.CharField(max_length=6, choices=GENDER, default=Null, null=True, blank=True) # usable for clothing and similar category
    images = GenericRelation(Image)
    status = models.CharField(max_length=MAX_LENGTHS['PRODUCT_STATUS'], choices=PRODUCT_STATUS_CHOICES, default=DEFAULTS['PRODUCT_STATUS'])
    tag = models.CharField(max_length=30,
                                    validators=[RegexValidator(regex=r'^[\'a-zA-Z0-9\s,-]*$',
                                    message=_("Allowed characters are - , ' and alphanumeric characters"),),], null=True, blank=True)

    class Meta:
        db_table = 'product'
        unique_together = ('product_code', 'company',)
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "name": self.name,
            "product_category": self.product_category.to_representation(),
            "brand_name": self.brand_name,
            "selling_price": self.selling_price,
            "selling_currency": self.selling_currency,
            "purchase_price": self.purchase_price,
            "purchase_currency": self.purchase_currency,
            "total_price": self.total_price,
            "link": self.link,
            'types': self.types
        }

    def to_represent_minimal(self, request=None):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "name": self.name,
            "product_category": self.product_category.to_representation(),
            "brand_name": self.brand_name,
            "link": self.link
        }

    def save(self, *args, **kwargs):
        ''' On save, add token, and check for bulk quantity and update price of product '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        if self.bulk_quantity:
            self.total_price = self.selling_price * self.bulk_quantity.quantity
        else:
            self.total_price = self.selling_price
        return super(Product, self).save(*args, **kwargs)

    def get_line_subtotal(self, quantity, voucher=None):
        if voucher:
            discount = voucher.coupon.discount
            discount_type = voucher.coupon.discount_type
            if discount_type == DISCOUNT_TYPE['PERCENTAGE']:
                discount = (discount / 100) * self.total_price
            return (float(self.total_price) * float(quantity)) - float(discount)
        else:
            return float(self.total_price) * float(quantity)

    def get_line_total(self, quantity, voucher=None):
        subtotal = self.get_line_subtotal(quantity, voucher)
        tax = self.company.tax if self.company.tax else 0
        service_charge = self.company.service_charge if self.company.service_charge else 0
        return

