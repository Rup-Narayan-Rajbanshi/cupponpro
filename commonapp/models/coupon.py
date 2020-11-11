import os
import shortuuid
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from commonapp.models.bill import Bill
from commonapp.models.company import Company
from commonapp.models.image import Image
from commonapp.encrypt import encrypt, decrypt
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from userapp.models.user import User
from django.dispatch import receiver

class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    description = models.CharField(max_length=250)
    expiry_date = models.DateField()
    token = models.CharField(max_length=8, editable=False)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(serialize=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_premium = models.BooleanField(default=False)
    images = GenericRelation(Image)
    deal_of_the_day = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupon'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        ''' on save, update token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        super(Coupon, self).save(*args, **kwargs)


class Voucher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=20, editable=False)
    is_redeem = models.BooleanField(default=False)
    watch_later = models.BooleanField(default=False)
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, null=True, blank=True)
    used_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'voucher'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.user.full_name + "-" + str(self.id)

    def save(self, *args, **kwargs):
        ''' on save, update token '''
        if not self.token:
            coupon_type = {
                'category': 'CC',
                'productcategory': 'PC',
                'product': 'SP'
            }
            uuid4 = shortuuid.ShortUUID().random(length=4)
            coupon_content_type = self.coupon.content_type.model
            coupon_type_token = self.coupon.content_object.token
            discount = self.coupon.discount
            discount = "0" + str(discount)
            discount = discount[-2:]
            key = self.coupon.company.key
            voucher_token = coupon_type[coupon_content_type] + coupon_type_token + discount + uuid4
            self.token = encrypt(voucher_token, key)
        super(Voucher, self).save(*args, **kwargs)  
