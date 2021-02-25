from django_filters import rest_framework as filters
from userapp.models.customer import Customer



class CustomerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name')
    phone_number = filters.CharFilter(field_name='phone_number')
    email  = filters.CharFilter(field_name='email')

    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email']