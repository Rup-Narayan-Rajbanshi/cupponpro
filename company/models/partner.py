import os
import uuid
from django.db import models
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from helpers.validators import is_alphanumeric_with_exception
from helpers.app_helpers import content_file_name, url_builder


class Partner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=32, validators=[is_alphanumeric_with_exception])
    link = models.URLField()
    logo = models.ImageField(upload_to=content_file_name)

    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        if self:
            logo = url_builder(self.logo, request)
            return {
                'id': self.id,
                'name': self.name,
                'link': self.link,
                'logo': logo
            }
        return self


@receiver(models.signals.post_delete, sender=Partner)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


@receiver(models.signals.pre_save, sender=Partner)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except:
        return False
    old_file = old_instance.logo
    new_file = instance.logo
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
