import uuid
from django.core.validators import RegexValidator
from django.db import models
from commonapp.models.company import Company
from userapp.models.user import User

class Bill(models.Model):
    ## these options needs to be moved in helpers/constant and choices variable and letter should be UPPER CASE
    # Payment Modes
    Card = 'Card'
    Cash = 'Cash'
    PAYMENT = [
        (Card, 'Card Payment'),
        (Cash, 'Cash Payment'),
    ]
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT, default=Cash)
    service_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    invoice_number = models.CharField(max_length=8, editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    ## need to revise as well, reve this as possible
    def save(self, *args, **kwargs):
        ''' Registered User's information saved, or saved from UI input '''
        if self.user:
            self.name = self.user.full_name
            self.email = self.user.email
            self.phone_number = self.user.phone_number
        if not self.service_charge:
            self.service_charge = self.company.service_charge
        if not self.tax:
            self.tax = self.company.tax
        if not self.invoice_number:
            company_obj = Company.objects.get(id=self.company_id)
            company_obj.invoice_counter += 1
            company_obj.save()
            invoice_number = str(company_obj.invoice_counter)
            self.invoice_number = "0" * (8 - len(invoice_number)) + invoice_number
        return super(Bill, self).save(*args, **kwargs)
