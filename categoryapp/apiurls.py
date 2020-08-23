# -*- coding:utf-8 -*-
from django.urls import path
from categoryapp.api.category import CategoryListView, CategoryDetailView, SubCategoryListView, SubCategoryDetailView, ProductCategoryListView


app_name = 'categoryapp'

urlpatterns = [
	path('category', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>', CategoryDetailView.as_view(), name='category_detail'),
    path('subcategory', SubCategoryListView.as_view(), name='subcategory_detail'),
    path('subcategory/<int:sub_category_id>', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    path('productcategory', ProductCategoryListView.as_view(), name='productcategory_list'),

    ]
