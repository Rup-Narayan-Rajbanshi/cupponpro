from django_filters import rest_framework as filters
from orderapp.models.order import Orders
from rest_framework.exceptions import ValidationError
from orderapp.models.transaction import TransactionHistoryBills

class OrdersFilter(filters.FilterSet):
    company = filters.CharFilter(field_name='company__id')
    from_date = filters.DateFilter(field_name='created_at__date',
                                    input_formats=['%Y-%m-%d','%d-%m-%Y'],
                                    lookup_expr='gte'
                                    )
    to_date = filters.DateFilter(field_name='created_at__date',
                                    input_formats=['%Y-%m-%d','%d-%m-%Y'],
                                    lookup_expr='lte'
                                    )
    status = filters.CharFilter(field_name='status')

    class Meta:
        model = Orders
        fields = ['company','status','from_date','to_date']
    
    @property
    def qs(self):
        parent = super(OrdersFilter, self).qs
        company = getattr(self.request, 'company', None)
        from_date = self.form.cleaned_data['from_date']
        to_date = self.form.cleaned_data['to_date']

        if from_date and to_date:
            if from_date > to_date:
                raise ValidationError({'detail':'From Date must be smaller than To Date'})
        return parent.filter(company=company)

from orderapp.models.bills import Bills

class ServiceChargeFilter(filters.FilterSet):
    from_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='lte')

    class Meta:
        model = Bills
        fields = ['from_date', 'to_date']

class SellItemFilter(filters.FilterSet):
    product_category = filters.CharFilter(field_name='orders__lines__product__product_category__name')
    from_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='lte')

    class Meta:
        model = Bills
        fields = ['product_category', 'from_date', 'to_date']

class BillFilter(filters.FilterSet):
    from_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name='created_at__date', lookup_expr='lte')
    invoice_number = filters.CharFilter(field_name='invoice_number')
    status = filters.BooleanFilter(field_name='is_paid')
    customer_name = filters.CharFilter(field_name='customer__name')

    class Meta:
        model = Bills
        fields = ['from_date','to_date','invoice_number','status','customer_name']

class TransactionFilter(filters.FilterSet):
    bill = filters.UUIDFilter(field_name='bill')

    class Meta:
        model = TransactionHistoryBills
        fields = ['bill']
