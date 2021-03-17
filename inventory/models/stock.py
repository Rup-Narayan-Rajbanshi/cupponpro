from django.db import models
from commonapp.models.company import Company
from helpers.models import BaseModel
from django.utils import timezone



class Stock(BaseModel):
    name = models.CharField(max_length=64)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=False, default=0)
    minimum_quantity = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=False, default=0)
    unit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        return {
            'id': self.id,
            'is_name': self.name
        }


