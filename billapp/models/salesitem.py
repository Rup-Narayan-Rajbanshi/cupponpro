from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from .bill import Bill
from productapp.models.product import Product


class SalesItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales_item'

    def __str__(self):
        return self.product.name + " of bill " + str(self.bill.id)