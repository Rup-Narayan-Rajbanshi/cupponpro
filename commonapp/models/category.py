import os
import shortuuid
from django.db import models
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    icon = models.FileField(upload_to='icons/', validators=[FileExtensionValidator(allowed_extensions=['svg'])])
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    token = models.CharField(max_length=8, editable=False, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, create token '''
        if not self.id:
            self.token = shortuuid.ShortUUID().random(length=8)
        return super(Category, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Category)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is defined.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    if instance.icon:
        if os.path.isfile(instance.icon.path):
            os.remove(instance.icon.path)


@receiver(models.signals.pre_save, sender=Category)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image_file = sender.objects.get(pk=instance.pk).image
        new_image_file = instance.image
        if old_image_file:
            if not old_image_file == new_image_file:
                if os.path.isfile(old_image_file.path):
                    os.remove(old_image_file.path)
    except:
        pass

    try:
        old_icon_file = sender.objects.get(pk=instance.pk).icon
        new_icon_file = instance.icon
        if old_icon_file:
            if not old_icon_file == new_icon_file:
                if os.path.isfile(old_icon_file.path):
                    os.remove(old_icon_file.path)
    except:
        pass

class SubCategory(models.Model):
    name = models.CharField(max_length=15, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "sub categories"

    def __str__(self):
        return self.name
