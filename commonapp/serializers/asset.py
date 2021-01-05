from rest_framework import serializers
from commonapp.models.asset import Asset
from helpers.constants import ORDER_LINE_STATUS


class AssetSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    served = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_qr(self, obj):
        return {
            'asset': obj.id,
            'company': obj.company_id
        }

    def get_order_id(self, obj):
        recent_order = obj.orders.order_by('-created_at').first()
        if recent_order:
            return recent_order.id
        return ''

    def get_order_status(self, obj):
        recent_order = obj.orders.order_by('-created_at').first()
        if recent_order:
            return recent_order.status
        return ''

    def get_orders(self, obj):
        latest_order = obj.orders.order_by('-created_at').first()
        return latest_order.lines.count() if latest_order else 0

    def get_served(self, obj):
        latest_order = obj.orders.order_by('-created_at').first()
        return latest_order.lines.filter(
            status=ORDER_LINE_STATUS['SERVED']).count() if latest_order else 0
