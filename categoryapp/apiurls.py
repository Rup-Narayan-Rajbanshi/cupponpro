# -*- coding:utf-8 -*-
from django.urls import path
from categoryapp.api.category import CategoryListView, ProductCategoryListView


app_name = 'categoryapp'

urlpatterns = [
	path('category', CategoryListView.as_view(), name='category_list'),
    path('productcategory', ProductCategoryListView.as_view(), name='productcategory_list'),

    ]
