import uuid
from django.core.validators import RegexValidator
from django.db import models
from commonapp.models.asset import Asset
from commonapp.models.bill import Bill
from commonapp.models.company import Company
from commonapp.models.coupon import Voucher
from commonapp.models.product import Product
from userapp.models.user import User

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=True,\
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    email = models.EmailField(max_length=50, null=False, blank=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)
    is_billed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        ''' Registered User's information saved, or saved from UI input '''
        if self.user:
            self.name = self.user.full_name
            self.email = self.user.email
            self.phone_number = self.user.phone_number
        return super(Order, self).save(*args, **kwargs)

class OrderLine(models.Model):
    # order states
    New = 'New'
    Progress = 'Progress'
    Completed = 'Completed'
    Cancelled = 'Cancelled'
    states = [
        (New, 'New'),
        (Progress, 'Progress'),
        (Completed, 'Completed'),
        (Cancelled, 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    rate = models.PositiveIntegerField(blank=True)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=20, choices=states, default=New)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_line'
        ordering = ['-created_at']

    def __str__(self):
        return "order " + str(self.id) + " of " + str(self.company.name)

    def save(self, *args, **kwargs):
        ''' On save, create key '''
        if not self.rate:
            self.rate = self.product.total_price
        return super(OrderLine, self).save(*args, **kwargs)
