from rest_framework import serializers
from commonapp.models.asset import Asset
from helpers.constants import ORDER_LINE_STATUS, ORDER_STATUS
from notifications.models import Notification


class AssetSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    notification_details = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_qr(self, obj):
        return {
            'asset': obj.id,
            'company': obj.company_id
        }

    def get_orders(self, obj):
        latest_order = obj.orders.filter(status__in=[
            ORDER_STATUS['NEW_ORDER'], ORDER_STATUS['PROCESSING'],
            ORDER_STATUS['CONFIRMED'], ORDER_STATUS['BILLABLE'], ]
        ).order_by('-created_at').first()
        return {
            "has_active_order": True if latest_order else False,
            "order_status": latest_order.status if latest_order else None,
            "total": latest_order.lines.count() if latest_order else 0,
            "served": latest_order.lines.filter(
                status=ORDER_LINE_STATUS['SERVED']).count() if latest_order else 0,
            "order_id": latest_order.id if latest_order else None,
            "total_amount": latest_order.subtotal if latest_order else 0
        }

    def get_notification_details(self, obj):
        request = self.context.get('request')
        if request:
            asset_notifications = obj.notification_set.filter(seen=False, user=request.user)
        else:
            asset_notifications = obj.notification_set.none()
        return {
            "has_active_notification": True if asset_notifications.exists() else False,
            "notifications": asset_notifications.values('payload', 'seen')
        }
