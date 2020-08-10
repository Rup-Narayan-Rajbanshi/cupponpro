# -*- coding:utf-8 -*-
from django.urls import path
from productapp.api.product import BulkQuantityListView, BulkQuantityDetailView, ProductListView, ProductDetailView

# from userapp.api.staticpage import StaticPageView

app_name = 'productapp'

urlpatterns = [
	path('bulkquantity', BulkQuantityListView.as_view(), name='bulkquantity_list'),
    path('bulkquantity/<int:bulk_quantity_id>', BulkQuantityDetailView.as_view(), name='bulkquantity_update'),
    path('product', ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>', ProductDetailView.as_view(), name='product_update'),
]