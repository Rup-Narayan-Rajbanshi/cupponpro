import os
import shortuuid
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.dispatch import receiver
from commonapp.models.image import Image
from commonapp.models.company import Company

class BulkQuantity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    name = models.CharField(max_length=30, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bulk_quantity'
        verbose_name_plural = "bulk quantities"

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    name = models.CharField(max_length=30, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_category/')
    token = models.CharField(max_length=8, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_category'
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name

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
    if instance.logo:
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

class Product(models.Model):
    Null = None
    Male = "M"
    Female = "F"
    Unisex = "U"
    GENDER = [
        (Null, ''),
        (Male, 'Male'),
        (Female, 'Female'),
        (Unisex, 'Unisex'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    product_code = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    brand_name = models.CharField(max_length=30, null=True, blank=True)
    unit_price = models.PositiveIntegerField()
    bulk_quantity = models.ForeignKey(BulkQuantity, on_delete=models.PROTECT, null=True, blank=True)
    total_price = models.PositiveIntegerField(editable=False)
    token = models.CharField(max_length=8, editable=False)
    is_veg = models.BooleanField(default=False) #only for food item
    gender = models.CharField(max_length=6, choices=GENDER, default=Null, null=True, blank=True) # usable for clothing and similar category
    images = GenericRelation(Image)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product'
        unique_together = ('product_code', 'company',)
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, add token, and check for bulk quantity and update price of product '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        if self.bulk_quantity:
            self.total_price = self.unit_price * self.bulk_quantity.quantity
        else:
            self.total_price = self.unit_price
        return super(Product, self).save(*args, **kwargs)
