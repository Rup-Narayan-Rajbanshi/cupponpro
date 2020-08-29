import shortuuid
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from billapp.models.bill import Bill
from commonapp.models.company import Company
from commonapp.models.image import Image
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from userapp.models.user import User

from userapp.models.user import User

class Coupon(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True)
    description = models.CharField(max_length=250)
    expiry_date = models.DateField()
    token = models.CharField(max_length=8, editable=False)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)])
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    is_premium = models.BooleanField(default=False)
    images = GenericRelation(Image)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'coupon'
    
    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        ''' on save, update token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=8)
        super(Coupon, self).save(*args, **kwargs)

class Voucher(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=20, null=True, editable=False)
    is_redeem = models.BooleanField(default=False)
    watch_later = models.BooleanField(default=False)
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, null=True, blank=True)
    save_amount = models.PositiveIntegerField(editable=False, null=True)
    used_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'voucher'
    
    def __str__(self):
        return self.user.full_name + "-" + str(self.id)