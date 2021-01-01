from rest_framework import serializers
from commonapp.models.asset import Asset
from helpers.constants import ORDER_LINE_STATUS


class AssetSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()
    orders = serializers.SerializerMethodField()
    served = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_qr(self, obj):
        return {
            'asset': obj.id,
            'company': obj.company_id
        }

    def get_order_status(self, obj):
        recent_order = obj.company.orders.order_by('-created_at')[:1]
        if recent_order:
            return recent_order[0].status
        return ''

    def get_orders(self, obj):
        return obj.company.orders.order_by('-created_at')[0].lines.count()

    def get_served(self, obj):
        return obj.company.orders.order_by('-created_at')[0].lines.filter(
            status=ORDER_LINE_STATUS['SERVED']).count()
