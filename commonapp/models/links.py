from django.db import models
from commonapp.models.company import Company

class SocialLink(models.Model):
    name = models.CharField(max_length=15)
    url = models.CharField(max_length=250)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'social_link'

    def __str__(self):
        return self.url