from billapp.models.bill import Bill
from rest_framework import serializers

class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'company', 'user', 'total', 'discount_percentage',\
            'discount', 'grand_total', 'created_at',)
        read_only_fields = ('created_at',)