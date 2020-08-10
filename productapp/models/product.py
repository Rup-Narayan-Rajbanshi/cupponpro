from django.db import models
from django.utils import timezone
from categoryapp.models.category import ProductCategory
from commonapp.models.company import Company
from userapp.models import User

class BulkQuantity(models.Model):
    name = models.CharField(max_length=30, unique=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'bulkquantity'
        verbose_name_plural = "bulk quantities"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(BulkQuantity, self).save(*args, **kwargs)

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    product_category= models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='product/', null=True, blank=True)
    bulk_quantity = models.ForeignKey(BulkQuantity, on_delete=models.PROTECT, null=True, blank=True)
    unit_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'product'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        if self.bulk_quantity:
            self.total_price = self.unit_price * self.bulk_quantity.quantity
        else:
            self.total_price = self.unit_price
        return super(Product, self).save(*args, **kwargs)