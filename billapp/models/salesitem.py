from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from .bill import Bill
from productapp.models.product import Product


class Salesitem(models.Model):
    # Currency Variables
    Null = None
    Nepali_Rupees = 'NPR'
    US_Dollar = 'USD'
    Indian_Rupees = 'INR'
    CURRENCY = [
        (Null, ''),
        (Nepali_Rupees, 'Nepali Rupees'),
        (US_Dollar, 'US Dollar'),
        (Indian_Rupees, 'Indian Rupees'),
    ]

    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, choices=CURRENCY, default=Null, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales_item'


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Salesitem, self).save(*args, **kwargs)