from django.db import models
from company.models.company import Company
from helpers.models import BaseModel


class Supplier(BaseModel):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        return {
            'id': self.id,
            'is_name': self.name
        }