# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.company import CompanyListView, CompanyInfoListView, CompanyInfoDetailView

# from userapp.api.staticpage import StaticPageView

app_name = 'commonapp'

urlpatterns = [
	path('companys', CompanyListView.as_view(), name='company_list'),
    path('companyinfo', CompanyInfoListView.as_view(), name='companyinfo_list'),
    path('companyinfo/<int:companyinfo_id>', CompanyInfoDetailView.as_view(), name='companyinfo_update'),
]