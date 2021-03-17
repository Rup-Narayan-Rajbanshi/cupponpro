import uuid
from django.db import models
from company.models.company import Company
from userapp.models.user import User

class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='company_rating')
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rate = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rating'
        ordering = ['-created_at']
