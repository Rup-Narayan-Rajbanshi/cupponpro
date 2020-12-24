from rest_framework import serializers
from commonapp.models.asset import Asset


class AssetSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField()
    order_status = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_qr(self, obj):
        return {
            'asset': obj.id,
            'company': obj.company_id
        }

    def get_order_status(self, obj):
        recent_order = obj.company.order_set.order_by('-id')[:1]
        if recent_order:
            return recent_order[0].status
        return ''
