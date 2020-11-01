import uuid
from django.db import models
from commonapp.models.company import Company

class Asset(models.Model):
    # asset types
    Room = 'Room'
    Table = 'Table'
    asset_types = [
        (Room, 'Room'),
        (Table, 'Table'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    asset_type = models.CharField(max_length=20, choices=asset_types, default=Room)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asset'
        ordering = ['-created_at']

    def __str__(self):
        return self.name + " of " + str(self.company.name)
