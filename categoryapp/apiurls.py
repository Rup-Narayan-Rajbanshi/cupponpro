# -*- coding:utf-8 -*-
from django.urls import path
from categoryapp.api.category import CategoryListView


app_name = 'categoryapp'

urlpatterns = [
	path('categories', CategoryListView.as_view(), name='category_list'),

    ]
