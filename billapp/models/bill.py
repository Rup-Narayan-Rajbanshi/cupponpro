from uuid import uuid4
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.utils import timezone
from commonapp.models.company import Company
from userapp.models.user import User


class Bill(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    total = models.PositiveIntegerField()
    discount_percentage = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'bill'


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Bill, self).save(*args, **kwargs)