from django_filters import rest_framework as filters
from orderapp.models.bills import Bills

class SalesFilter(filters.FilterSet):
    types = filters.CharFilter(field_name='orders__lines__product__product_category__types')
    from_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='lte')
    class meta:
        model = Bills
        field = ['types', 'from_date', 'to_date']
