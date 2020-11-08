import uuid
from django.core.validators import RegexValidator
from django.db import models
from commonapp.models.company import Company
from userapp.models.user import User

class Bill(models.Model):
    # Payment Modes
    Card = 'Card'
    Cash = 'Cash'
    PAYMENT = [
        (Card, 'Card Payment'),
        (Cash, 'Cash Payment'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=True,\
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    email = models.EmailField(max_length=50, null=False, blank=True)
    tax = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT, default=Cash)
    paid_amount = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bill'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        ''' Registered User's information saved, or saved from UI input '''
        if self.user:
            self.name = self.user.full_name
            self.email = self.user.email
            self.phone_number = self.user.phone_number
        return super(Bill, self).save(*args, **kwargs)
