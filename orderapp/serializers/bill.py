from django.db.models import Sum

from helpers.serializer import CustomModelSerializer
from orderapp.models.bills import Bills


class BillCreateSerializer(CustomModelSerializer):

    class Meta:
        model = Bills
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
