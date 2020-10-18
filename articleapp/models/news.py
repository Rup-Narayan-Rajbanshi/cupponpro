import os
import uuid
from django.db import models
from django.dispatch import receiver

class NewsArticle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    news_partner = models.CharField(max_length=50)
    url = models.TextField()
    headline = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='news/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'news_article'

    def __str__(self):
        return self.headline

@receiver(models.signals.post_delete, sender=NewsArticle)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
        
@receiver(models.signals.pre_save, sender=NewsArticle)
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