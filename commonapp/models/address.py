from django.db import models

class Address(models.Model):
    country = models.CharField(max_length=30, null=False, blank=False)
    state = models.CharField(max_length=30, null=False, blank=False)
    city = models.CharField(max_length=30, null=False, blank=False)
    address = models.CharField(max_length=30, null=False, blank=False)
    zip_code = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        db_table = 'address'
        abstract = True
