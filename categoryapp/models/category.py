import shortuuid
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
import os
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    icon = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    token = models.CharField(max_length=8, editable=False, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, add token '''
        if not self.id:
            self.token = shortuuid.ShortUUID().random(length=8)
        return super(Category, self).save(*args, **kwargs)

class SubCategory(models.Model):
    name = models.CharField(max_length=15, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subcategory'
        verbose_name_plural = "sub categories"

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(editable=False)
    token = models.CharField(max_length=8, editable=False, null=False, blank=True)

    class Meta:
        db_table = 'productcategory'
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
            self.token = shortuuid.ShortUUID().random(length=8)
        return super(ProductCategory, self).save(*args, **kwargs)
