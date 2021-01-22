from django.db import models

class Address(models.Model):
    country = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=30, null=False, blank=False)
    zip_code = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'address'
        abstract = True
