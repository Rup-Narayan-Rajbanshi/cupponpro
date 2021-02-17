from helpers.models import BaseModel
from django.db import models
from orderapp.models.bills import Bills



class TransactionHistoryBills(BaseModel):
    bill = models.ForeignKey(Bills, on_delete=models.CASCADE, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    return_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    net_paid_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=False, default=0)

    def save(self, *args, **kwargs):
        self.net_paid_amount = float(self.paid_amount) - float(self.return_amount)
        return super(TransactionHistoryBills, self).save(*args, **kwargs)