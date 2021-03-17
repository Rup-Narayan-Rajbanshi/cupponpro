import uuid
from django.db import models
from company.models.company import Company
from helpers.choices_variable import ASSET_TYPE_CHOICES
from helpers.constants import ASSET_TYPE


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, default=ASSET_TYPE['ROOM'])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asset'
        ordering = ['-created_at']

    def __str__(self):
        return self.name + " of " + str(self.company.name)

    def to_representation(self, request=None):
        if self:
            return {
                'id': self.id,
                'name': self.name,
                'asset_type': self.asset_type
            }
        return None

    def to_representation_detail(self, request=None):
        if self:
            return {
                'id': self.id,
                'name': self.name,
                'asset_type': self.asset_type,
                'company': self.company.to_representation() if self.company else None
            }
        return None
