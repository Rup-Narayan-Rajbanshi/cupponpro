import uuid
from django.db import models, transaction
from helpers.models import BaseModel
from helpers.constants import OTP_TYPES, OTP_STATUS_TYPES, MAX_LENGTHS, DEFAULTS


class OrderScanLog(BaseModel):
    asset = models.ForeignKey(
        'commonapp.Asset',
        on_delete=models.CASCADE,
        related_name='asset_scan_log'
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    @classmethod
    @transaction.atomic
    def create_scan_log(cls, **kwargs):
        log = cls.objects.create(**kwargs)
        return log
