from django.db import models
from django.utils import timezone
from commonapp.models.company import Company
from userapp.models.user import User
from django.core.validators import RegexValidator

class Bill(models.Model):
    # Payment Modes
    Card = 'Card'
    Cash = 'Cash'
    PAYMENT = [
        (Card, 'Card Payment'),
        (Cash, 'Cash Payment'),
    ]

    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True,\
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    email = models.EmailField(max_length=50, null=False, blank=True)
    total = models.PositiveIntegerField()
    total_discount = models.PositiveIntegerField(null=True)
    tax = models.PositiveIntegerField()
    taxed_amount = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT, default=Cash)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'bill'

    def save(self, *args, **kwargs):
        ''' Registered User's information saved, or saved from UI input '''
        if self.user:
            self.name = self.user.full_name
            self.email = self.user.email
            self.phone_number = self.user.phone_number
        return super(Bill, self).save(*args, **kwargs)