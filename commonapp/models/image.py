import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os

class Image(models.Model):

    def get_upload_path(self, filename):
        return '{}/{}'.format(self.content_type.model_class().__name__.lower(), filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    image = models.ImageField(upload_to=get_upload_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image'
        ordering = ['-created_at']

    def __str__(self):
        return os.path.basename(self.image.name)
