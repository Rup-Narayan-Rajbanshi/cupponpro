from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import DetailRelatedField
from helpers.serializer import CustomModelSerializer
from helpers.constants import ORDER_STATUS, ORDER_SCAN_COOLDOWN
from commonapp.models.asset import Asset
from commonapp.models.order import Order
from orderapp.models.order_scan_log import OrderScanLog
from helpers.exceptions import OrderScanCooldownException


class ValidateOrderScanSerializer(CustomModelSerializer):
    asset = DetailRelatedField(model=Asset, lookup='id', representation='to_representation_detail')
    token = serializers.UUIDField(read_only=True)
    scan_cooldown = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.order = None
        self.scan_log = None
        self.current_datetiem = timezone.now()
        super().__init__(*args, **kwargs)

    class Meta:
        model = OrderScanLog
        fields = ('asset', 'token', 'scan_cooldown')

    def validate(self, attrs):
        asset = attrs.get('asset')
        self.order = Order.objects.filter(
                            asset=asset,
                            status__in=[ORDER_STATUS['NEW_ORDER'], ORDER_STATUS['CONFIRMED'], ORDER_STATUS['PROCESSING']]).exists()
        if not self.order:
            now  = self.current_datetiem
            earlier_time = now - timedelta(minutes=ORDER_SCAN_COOLDOWN)
            self.scan_log = OrderScanLog.objects.filter(created_at__range=[earlier_time, now], asset=asset).order_by('-created_at').first()
            # if self.scan_log:
            #     raise OrderScanCooldownException()
        return attrs

    def get_scan_cooldown(self, obj):
        if not self.order:
            scan_cooldown = ORDER_SCAN_COOLDOWN * 60
            if self.scan_log:
                scan_diff = self.current_datetiem - self.scan_log.created_at
                scan_diff_second = scan_diff.seconds
                scan_cooldown = scan_cooldown - scan_diff_second
                scan_cooldown = 0 if scan_cooldown < 0 else scan_cooldown
            return scan_cooldown
        return 0

    def create(self, v_data):
        request = self.context.get('request')
        if self.scan_log:
            self.scan_log.token = None
            return self.scan_log
        log = OrderScanLog.create_scan_log(**v_data)
        return log
