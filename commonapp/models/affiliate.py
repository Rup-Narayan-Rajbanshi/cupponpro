import uuid
from django.db import models
from commonapp.models.company import Company
from commonapp.models.category import Category, SubCategory

class AffiliateLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
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
    deal_of_the_day = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'affiliate_link'
        ordering = ['-created_at']

    def __str__(self):
        return self.description

    def add_count(self):
        ''' function to add count by 1 when user visit the link. '''
        self.count += 1
        self.save()
