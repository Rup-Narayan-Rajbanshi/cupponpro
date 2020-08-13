from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from commonapp.models.company import Company
from userapp.models.user import User


class Rating(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rate = models.PositiveIntegerField()
    created_at = models.DateTimeField(editable=False)

    class Meta:
        db_table = 'rating'


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        return super(Rating, self).save(*args, **kwargs)