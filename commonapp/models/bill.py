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
    invoice_number = models.CharField(max_length=8, editable=False)
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
        if not self.invoice_number:
            company_obj = Company.objects.get(id=self.company_id)
            company_obj.invoice_counter += 1
            company_obj.save()
            invoice_number = str(company_obj.invoice_counter)
            self.invoice_number = "0" * (8 - len(invoice_number)) + invoice_number
        return super(Bill, self).save(*args, **kwargs)
