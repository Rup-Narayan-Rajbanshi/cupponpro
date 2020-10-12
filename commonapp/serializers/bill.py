from commonapp.models.bill import Bill
from rest_framework import serializers

class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = '__all__'