from django.urls import path
from billapp.api.bill import BillListView, BillDetailView
from billapp.api.salesitem import SalesitemListView

app_name = 'billapp'

urlpatterns = [
    path('bill/', BillListView.as_view(), name='bill_list'),
    path('bill/<int:bill_id>/', BillDetailView.as_view(), name='bill_detail'),
    path('bill/<int:bill_id>/salesitem/', SalesitemListView.as_view(), name='sales_item_list'),
]