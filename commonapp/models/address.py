from django.db import models

class Address(models.Model):
    country = models.CharField(max_length=30, default='', blank=True)
    state = models.CharField(max_length=30, default='', blank=True)
    city = models.CharField(max_length=30, default='', blank=True)
    address = models.CharField(max_length=30, default='', blank=True)
    zip_code = models.CharField(max_length=30, default='', blank=True)

    class Meta:
        db_table = 'address'
        abstract = True
