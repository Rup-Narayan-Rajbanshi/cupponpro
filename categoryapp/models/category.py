from uuid import uuid4
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
import os
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(editable=False)


    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Category, self).save(*args, **kwargs)

class ProductCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'productcategory'
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(ProductCategory, self).save(*args, **kwargs)
