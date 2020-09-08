# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.affiliate import AffiliateLinkListView, AffiliateLinkDetailView, AffiliateLinkCountView
from commonapp.api.category import CategoryListView, CategoryDetailView, SubCategoryListView, SubCategoryDetailView
from commonapp.api.company import CompanyListView, CompanyDetailView, CompanyUserListView, PartnerListView, CompanyFavouriteView, CompanyCreateView
from commonapp.api.coupon import CouponListView, CouponDetailView, CategoryCouponListView, CouponTypeListView, VoucherListView
from commonapp.api.document import CompanyDocumentListView, CompanyDocumentDetailView
from commonapp.api.facility import CompanyFacilityListView, CompanyFacilityDetailView
from commonapp.api.rating import CompanyRatingListView, CompanyRatingDetailView
from commonapp.api.search import TopBarSearchView

app_name = 'commonapp'

urlpatterns = [
    # category
    path('category', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>', CategoryDetailView.as_view(), name='category_detail'),
    path('subcategory', SubCategoryListView.as_view(), name='subcategory_detail'),
    path('subcategory/<int:sub_category_id>', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    # company
	path('company', CompanyListView.as_view(), name='company_list'),
    path('company/create', CompanyCreateView.as_view(), name='company_create'),
    path('company/<int:company_id>', CompanyDetailView.as_view(), name='company_detail'),
    path('partner', PartnerListView.as_view(), name='partner_company_list'),
    path('company/<int:company_id>/user', CompanyUserListView.as_view(), name='company_user_list'),
    path('company/<int:company_id>/favourite', CompanyFavouriteView.as_view(), name='company_favourite_list'),
    # document
    path('company/<int:company_id>/document', CompanyDocumentListView.as_view(), name='company_document_list'),
    path('company/<int:company_id>/document/<int:document_id>', CompanyDocumentDetailView.as_view(), name='company_document_detail'),
    # coupon
    path('coupon', CouponListView.as_view(), name='coupon_list'),
    path('coupon/<int:coupon_id>', CouponDetailView.as_view(), name='coupon_detail'),
    path('category/<int:category_id>/coupon', CategoryCouponListView.as_view(), name='category_coupon_list'),
    path('coupon/type', CouponTypeListView.as_view(), name='coupon_type_list'),
    # voucher
    path('voucher', VoucherListView.as_view(), name='voucher_list'),
    # rating
    path('company/<int:company_id>/rating', CompanyRatingListView.as_view(), name='company_rating_list'),
    path('company/<int:company_id>/rating/<int:rating_id>', CompanyRatingDetailView.as_view(), name='company_rating_detail'),
    # facility
    path('company/<int:company_id>/facility', CompanyFacilityListView.as_view(), name='company_facility_list'),
    path('company/<int:company_id>/facility/<int:facility_id>', CompanyFacilityDetailView.as_view(), name='company_facility_detail'),
    # affiliate
    path('affiliate', AffiliateLinkListView.as_view(), name='affiliate_link_list'),
    path('affiliate/<int:affiliate_link_id>', AffiliateLinkDetailView.as_view(), name='affiliate_link_detail'),
    path('affiliate/<int:affiliate_link_id>/addcount', AffiliateLinkCountView.as_view(), name='affiliate_link_add_count'),
    # search
    path('topbarsearch', TopBarSearchView.as_view(), name='top_bar_search_list'),
]