from django.db import models
from commonapp.models.company import Company
from commonapp.models.category import Category, SubCategory

class AffiliateLink(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    url = models.TextField(null=True, blank=True)
    discount_code = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='affiliate/', null=True, blank=True)
    description = models.TextField()
    discount = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'affiliate_link'

    def __str__(self):
        return self.description

    def add_count(self):
        self.count += 1
        self.save()
