from billapp.models.bill import Bill
from rest_framework import serializers

class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'company', 'user', 'name', 'phone_number',\
            'total', 'total_discount', 'tax', 'taxed_amount', 'payment_mode', \
            'grand_total', 'created_at',)
        read_only_fields = ('created_at',)