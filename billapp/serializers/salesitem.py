from billapp.models.salesitem import Salesitem
from rest_framework import serializers

class SalesitemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Salesitem
        fields = ('id', 'bill', 'product', 'amount', 'quantity', 'currency', 'created_at')
        read_only_fields = ('created_at',)