from django.db import models
from commonapp.models.company import Company

class Facility(models.Model):
    name = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = "facilities"

    def __str__(self):
        return self.name