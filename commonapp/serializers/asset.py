from rest_framework import serializers
from commonapp.models.asset import Asset
from helpers.constants import ORDER_LINE_STATUS


class AssetSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_qr(self, obj):
        return {
            'asset': obj.id,
            'company': obj.company_id
        }

    def get_orders(self, obj):
        latest_order = obj.orders.order_by('-created_at').first()
        return {
            "has_active_order": True if latest_order else False,
            "order_status": latest_order.status if latest_order else None,
            "total": latest_order.lines.count() if latest_order else 0,
            "served": latest_order.lines.filter(
                status=ORDER_LINE_STATUS['SERVED']).count() if latest_order else 0,
            "order_id": latest_order.id if latest_order else None
        }
