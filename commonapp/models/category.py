import shortuuid
from django.db import models
from django.core.validators import FileExtensionValidator

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

class SubCategory(models.Model):
    name = models.CharField(max_length=15, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sub_category'
        verbose_name_plural = "sub categories"

    def __str__(self):
        return self.name
