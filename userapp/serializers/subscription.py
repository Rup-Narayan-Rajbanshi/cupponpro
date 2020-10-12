from rest_framework import serializers
from userapp.models.subscription import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'