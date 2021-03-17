from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from inventory.models.purchase import Purchase




class PurchaseFilter(filters.FilterSet):
    types = filters.CharFilter(field_name='types')

    class Meta:
        model = Purchase
        fields = ['types']