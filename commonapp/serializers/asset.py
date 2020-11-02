from rest_framework import serializers
from commonapp.models.asset import Asset

class AssetSerializer(serializers.ModelSerializer):
    qr = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = "__all__"

    def get_qr(self, obj):
        return {
            'asset': obj.id,
            'company': obj.company_id
        }