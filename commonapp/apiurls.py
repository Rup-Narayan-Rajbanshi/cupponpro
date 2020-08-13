# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.company import CompanyListView, CouponListView, CouponDetailView

# from userapp.api.staticpage import StaticPageView

app_name = 'commonapp'

urlpatterns = [
	path('companys', CompanyListView.as_view(), name='company_list'),
    path('coupon', CouponListView.as_view(), name='coupon_list'),
    path('coupon/<int:coupon_id>', CouponDetailView.as_view(), name='coupon_update'),
]