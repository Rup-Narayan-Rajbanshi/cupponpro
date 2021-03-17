from django.db import models
from commonapp.models.company import Company
from helpers.models import BaseModel
from django.utils import timezone
from helpers.choices_variable import PAYMENT_CHOICES
from helpers.constants import DEFAULTS



class Expense(BaseModel):
    expense_for = models.CharField(max_length=128, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    document = models.FileField(upload_to="document/", blank=True, null=True)
    is_refund = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=False, default=0)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return self.expense_for




class Payment(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=False, default=0)
    paid_date = models.DateTimeField(default=timezone.now)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])
    payment_note = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return str(self.amount)