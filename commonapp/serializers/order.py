from rest_framework import serializers
from commonapp.models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
