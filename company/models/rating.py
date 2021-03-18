import uuid
from django.db import models
from company.models.company import Company
from userapp.models.user import User
from helpers.models import BaseModel

class Rating(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='company_rating')
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rate = models.DecimalField(max_digits=2, decimal_places=1)
  

    class Meta:
        db_table = 'rating'
        ordering = ['-created_at']
