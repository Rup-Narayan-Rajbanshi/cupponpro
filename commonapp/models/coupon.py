import shortuuid
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from commonapp.models.company import Company
from commonapp.models.image import  Image

class Coupon(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    token = models.CharField(max_length=8, editable=False, null=False, blank=True)
    token_expiry_date = models.DateField()
    discount = models.PositiveIntegerField()
    product_name = models.CharField(max_length=50, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    images = GenericRelation(Image)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupon'
    
    def __str__(self):
        return self.company.name

    def save(self, *args, **kwargs):
        ''' on save, update token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        super(Coupon, self).save(*args, **kwargs)