from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from .bill import Bill
from productapp.models.product import Product


class Salesitem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales_item'


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Salesitem, self).save(*args, **kwargs)