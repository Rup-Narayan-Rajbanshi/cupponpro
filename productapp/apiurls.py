# -*- coding:utf-8 -*-
from django.urls import path
from productapp.api.product import BulkQuantityListView, BulkQuantityDetailView, ProductListView, ProductDetailView, ProductCategoryListView, CompanyProductCategoryListView

# from userapp.api.staticpage import StaticPageView

app_name = 'productapp'

urlpatterns = [
	path('company/<int:company_id>/bulkquantity', BulkQuantityListView.as_view(), name='company_bulkquantity_list'),
    path('company/<int:company_id>/bulkquantity/<int:bulk_quantity_id>', BulkQuantityDetailView.as_view(), name='bulkquantity_update'),
    path('product', ProductListView.as_view(), name='product_list'),
    path('product/<int:product_id>', ProductDetailView.as_view(), name='product_update'),
    path('productcategory', ProductCategoryListView.as_view(), name='product_category_list'),
    path('company/<int:company_id>/productcategory', CompanyProductCategoryListView.as_view(), name='company_product_category_list'),
]