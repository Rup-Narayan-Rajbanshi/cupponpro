from django.urls import path
from billapp.api.bill import BillListView
from billapp.api.salesitem import SalesitemListView

app_name = 'billapp'

urlpatterns = [
    path('bill', BillListView.as_view(), name='bill_list'),
    path('salesitem/', SalesitemListView.as_view(), name='salesitem'),
]