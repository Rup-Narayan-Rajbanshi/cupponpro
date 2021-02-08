from helpers.serializer import CustomModelSerializer
from userapp.models.customer import Customer

class CustomerSerializer(CustomModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"