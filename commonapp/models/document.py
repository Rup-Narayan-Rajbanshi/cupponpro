from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from commonapp.models.company import Company
from commonapp.models.image import Image

class Document(models.Model):
    name = models.CharField(max_length=50)
    images = GenericRelation(Image)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'document'

    def __str__(self):
        return self.name