import os
import uuid
from django.db import models
from django.dispatch import receiver
from helpers.models import BaseModel

class Blog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    description = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Blog)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
        
@receiver(models.signals.pre_save, sender=Blog)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except:
        return False
    
    new_file = instance.image
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)