import uuid
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from commonapp.models.bill import Bill
from commonapp.models.product import Product
from commonapp.models.coupon import Voucher
from commonapp.models.order import OrderLine

class SalesItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(OrderLine, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    voucher = models.ForeignKey(Voucher, on_delete=models.PROTECT, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sales_item'
        ordering = ['-created_at']

    def __str__(self):
        return self.product.name + " of bill " + str(self.bill.id)
