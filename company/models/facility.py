import uuid
from django.db import models
from company.models.company import Company

class Facility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    name = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'facility'
        verbose_name_plural = "facilities"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
