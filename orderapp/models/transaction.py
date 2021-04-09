from helpers.models import BaseModel
from django.db import models
from orderapp.models.bills import Bills
from orderapp.constants import DEFAULTS
from orderapp.choice_variables import PAYMENT_CHOICES
from userapp.models.user import User
from orderapp.models.order import Orders


class TransactionHistoryBills(BaseModel):
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    return_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    net_paid_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default=DEFAULTS['PAYMENT_CHOICES'])

    def save(self, *args, **kwargs):
        self.net_paid_amount = float(self.paid_amount) - float(self.return_amount)
        return super(TransactionHistoryBills, self).save(*args, **kwargs)



class Complimentary(BaseModel):
    order = models.OneToOneField(Orders, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
