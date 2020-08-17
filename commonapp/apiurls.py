# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.company import CompanyListView
from commonapp.api.coupon import CouponListView, CouponDetailView, CategoryCouponListView
from commonapp.api.rating import CompanyRatingListView, CompanyRatingDetailView

app_name = 'commonapp'

urlpatterns = [
	path('company', CompanyListView.as_view(), name='company_list'),
    path('coupon', CouponListView.as_view(), name='coupon_list'),
    path('coupon/<int:coupon_id>', CouponDetailView.as_view(), name='coupon_update'),
    path('company/<int:company_id>/rating', CompanyRatingListView.as_view(), name='company_rating_list'),
    path('company/<int:company_id>/rating/<int:rating_id>', CompanyRatingDetailView.as_view(), name='company_rating_list'),
    path('category/<int:category_id>/coupon', CategoryCouponListView.as_view(), name='category_coupon_list'),
]