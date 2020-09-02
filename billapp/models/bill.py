from django.db import models
from django.utils import timezone
from commonapp.models.company import Company
from userapp.models.user import User


class Bill(models.Model):
    # Currency Variables
    Null = None
    Nepali_Rupees = 'NPR'
    US_Dollar = 'USD'
    Indian_Rupees = 'INR'
    CURRENCY = [
        (Null, ''),
        (Nepali_Rupees, 'Nepali Rupees'),
        (US_Dollar, 'US Dollar'),
        (Indian_Rupees, 'Indian Rupees'),
    ]

    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=10, null=True)
    total = models.PositiveIntegerField()
    total_discount = models.PositiveIntegerField(null=True)
    tax = models.PositiveIntegerField()
    taxed_amount = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=10, choices=CURRENCY, default=Null, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'bill'


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Bill, self).save(*args, **kwargs)