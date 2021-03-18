import uuid
from django.db import models
from company.models.company import Company
from helpers.models import BaseModel

class SocialLink(BaseModel):
    name = models.CharField(max_length=15)
    url = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'social_link'
        ordering = ['-created_at']

    def __str__(self):
        return self.url
