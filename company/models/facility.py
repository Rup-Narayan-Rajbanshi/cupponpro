import uuid
from django.db import models
from company.models.company import Company
from helpers.models import BaseModel

class Facility(BaseModel):
    name = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = "facilities"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
