from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from commonapp.models.image import Image
from commonapp.models.company import Company
from userapp.models import User

class BulkQuantity(models.Model):
    name = models.CharField(max_length=30, unique=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'bulk_quantity'
        verbose_name_plural = "bulk quantities"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(BulkQuantity, self).save(*args, **kwargs)

class ProductCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.CharField(max_length=8, editable=False, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_category'
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, create token '''
        if not self.id:
            self.token = shortuuid.ShortUUID().random(length=8)
        return super(ProductCategory, self).save(*args, **kwargs)

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    images = GenericRelation(Image)
    bulk_quantity = models.ForeignKey(BulkQuantity, on_delete=models.PROTECT, null=True, blank=True)
    unit_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(editable=False)
    token = models.CharField(max_length=8, editable=False, null=False, blank=True)

    class Meta:
        db_table = 'product'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
            self.token = shortuuid.ShortUUID().random(length=8)
        if self.bulk_quantity:
            self.total_price = self.unit_price * self.bulk_quantity.quantity
        else:
            self.total_price = self.unit_price
        return super(Product, self).save(*args, **kwargs)