# -*- coding:utf-8 -*-
from django.urls import path
from productapp.api.product import (
    CompanyBulkQuantityListView,
    CompanyBulkQuantityDetailView,
    CompanyProductListView,
    CompanyProductDetailView,
    ProductCategoryListView,
    CompanyProductCategoryListView,
)

app_name = 'productapp'

urlpatterns = [
	path('company/<int:company_id>/bulkquantity', CompanyBulkQuantityListView.as_view(), name='company_bulkquantity_list'),
    path('company/<int:company_id>/bulkquantity/<int:bulk_quantity_id>', CompanyBulkQuantityDetailView.as_view(), name='company_bulkquantity_update'),
    path('company/<int:company_id>/product', CompanyProductListView.as_view(), name='company_product_list'),
    path('company/<int:company_id>/product/<int:product_id>', CompanyProductDetailView.as_view(), name='company_product_update'),
    path('productcategory', ProductCategoryListView.as_view(), name='product_category_list'),
    path('company/<int:company_id>/productcategory', CompanyProductCategoryListView.as_view(), name='company_product_category_list'),
]