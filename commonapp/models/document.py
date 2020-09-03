from django.core.validators import FileExtensionValidator
from django.db import models
from commonapp.models.company import Company
from commonapp.models.image import Image

class Document(models.Model):
    name = models.CharField(max_length=50)
    document_number = models.CharField(max_length=50, null=True, blank=True)
    document = models.FileField(upload_to="document/", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])])
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'document'

    def __str__(self):
        return self.name
