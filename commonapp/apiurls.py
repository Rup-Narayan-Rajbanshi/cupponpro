# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.company import CompanyListView, CompanyInfoListView

# from userapp.api.staticpage import StaticPageView

app_name = 'commonapp'

urlpatterns = [
	path('companys', CompanyListView.as_view(), name='company_list'),
    path('companyinfo/<int:company_id>', CompanyInfoListView.as_view(), name='company_info'),

    ]
