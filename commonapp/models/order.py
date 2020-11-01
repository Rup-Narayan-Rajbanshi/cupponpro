import uuid
from django.db import models
from commonapp.models.asset import Asset
from commonapp.models.company import Company
from commonapp.models.product import Product

class Order(models.Model):
    # order states
    New = 'New'
    Progress = 'Progress'
    Completed = 'Ccompleted'
    Cancelled = 'Cancelled'
    states = [
        (New, 'New'),
        (Progress, 'Progress'),
        (Completed, 'Completed'),
        (Cancelled, 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    rate = models.PositiveIntegerField(blank=True)
    quantity = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=states, default=New)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        return "order " + str(self.id) + " of " + str(self.company.name)

    def save(self, *args, **kwargs):
        ''' On save, create key '''
        if not self.rate:
            self.rate = self.product.total_price
        return super(Order, self).save(*args, **kwargs)
