# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.company import CompanyListView, CompanyUserListView, PartnerListView, CompanyFavouriteView
from commonapp.api.coupon import CouponListView, CouponDetailView, CategoryCouponListView
from commonapp.api.rating import CompanyRatingListView, CompanyRatingDetailView

app_name = 'commonapp'

urlpatterns = [
	path('company', CompanyListView.as_view(), name='company_list'),
    path('partner', PartnerListView.as_view(), name='partner_company_list'),
    path('coupon', CouponListView.as_view(), name='coupon_list'),
    path('coupon/<int:coupon_id>', CouponDetailView.as_view(), name='coupon_detail'),
    path('company/<int:company_id>/user', CompanyUserListView.as_view(), name='company_user_list'),
    path('company/<int:company_id>/favourite', CompanyFavouriteView.as_view(), name='company_favourite_list'),
    path('company/<int:company_id>/rating', CompanyRatingListView.as_view(), name='company_rating_list'),
    path('company/<int:company_id>/rating/<int:rating_id>', CompanyRatingDetailView.as_view(), name='company_rating_detail'),
    path('category/<int:category_id>/coupon', CategoryCouponListView.as_view(), name='category_coupon_list'),
]