from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from commonapp.models.company import Company
from userapp.models.user import User


class Rating(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'rating'