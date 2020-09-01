from django.db import models
from commonapp.models.company import Company
from commonapp.models.category import Category, SubCategory

class AffiliateLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    url = models.TextField()
    image = models.ImageField(upload_to='affiliate/')
    description = models.TextField()
    discount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'affiliate_link'

    def __str__(self):
        return self.description
