from billapp.models.salesitem import SalesItem
from rest_framework import serializers

class SalesItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalesItem
        fields = ('id', 'bill', 'product', 'amount', 'quantity', 'currency', 'created_at')
        read_only_fields = ('created_at',)