# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.affiliate import AffiliateLinkListView, AffiliateLinkDetailView, AffiliateLinkCountView,\
    TopDiscountAffiliateListView
from commonapp.api.bill import BillListView, BillDetailView
from commonapp.api.category import CategoryListView, CategoryDetailView, SubCategoryListView, SubCategoryDetailView
from commonapp.api.company import CompanyListView, CompanyDetailView, CompanyUserListView, PartnerListView,\
    CompanyFavouriteView, ChangeCompanyEmailView, CategoryCompanyListView
from commonapp.api.coupon import CouponListView, CouponDetailView, CategoryCouponListView, CouponTypeListView,\
    VoucherListView, TrendingCouponListView
from commonapp.api.document import CompanyDocumentListView, CompanyDocumentDetailView, CompanyDocumentMassUpdateView
from commonapp.api.facility import CompanyFacilityListView, CompanyFacilityDetailView
from commonapp.api.image import CompanyImageListView, CompanyImageDetailView
from commonapp.api.links import SocialLinkListView, SocialLinkDetailView, SocialLinkMassUpdateView
from commonapp.api.product import (
    CompanyBulkQuantityListView,
    CompanyBulkQuantityDetailView,
    CompanyProductListView,
    CompanyProductDetailView,
    ProductCategoryListView,
    CompanyProductCategoryListView,
)
from commonapp.api.rating import CompanyRatingListView, CompanyRatingDetailView
from commonapp.api.salesitem import SalesItemListView
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
    path('company/<int:company_id>', CompanyDetailView.as_view(), name='company_detail'),
    path('partner', PartnerListView.as_view(), name='partner_company_list'),
    path('company/<int:company_id>/user', CompanyUserListView.as_view(), name='company_user_list'),
    path('company/<int:company_id>/favourite', CompanyFavouriteView.as_view(), name='company_favourite_list'),
    path('company/<int:company_id>/email', ChangeCompanyEmailView.as_view(), name='update_company_email'),
    path('category/<int:category_id>/company', CategoryCompanyListView.as_view(), name='category_company_list'),
    # company image
    path('company/<int:company_id>/image', CompanyImageListView.as_view(), name='company_image_list'),
    path('company/<int:company_id>/image/<int:image_id>', CompanyImageDetailView.as_view(), name='company_image_detail'),
    # document
    path('company/<int:company_id>/document', CompanyDocumentListView.as_view(), name='company_document_list'),
    path('company/<int:company_id>/document/<int:document_id>', CompanyDocumentDetailView.as_view(), name='company_document_detail'),
    path('company/<int:company_id>/document/update', CompanyDocumentMassUpdateView.as_view(), name='company_document_mass_update'),
    # coupon
    path('coupon', CouponListView.as_view(), name='coupon_list'),
    path('coupon/<int:coupon_id>', CouponDetailView.as_view(), name='coupon_detail'),
    path('category/<int:category_id>/coupon', CategoryCouponListView.as_view(), name='category_coupon_list'),
    path('coupon/type', CouponTypeListView.as_view(), name='coupon_type_list'),
    path('coupon/trending', TrendingCouponListView.as_view(), name='trending_coupon_list'),
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
    path('affiliate/top-discount', TopDiscountAffiliateListView.as_view(), name='top_discount_affiliate_link'),
    # search
    path('topbarsearch', TopBarSearchView.as_view(), name='top_bar_search_list'),
    # product
    path('company/<int:company_id>/bulkquantity', CompanyBulkQuantityListView.as_view(), name='company_bulkquantity_list'),
    path('company/<int:company_id>/bulkquantity/<int:bulk_quantity_id>', CompanyBulkQuantityDetailView.as_view(), name='company_bulkquantity_update'),
    path('company/<int:company_id>/product', CompanyProductListView.as_view(), name='company_product_list'),
    path('company/<int:company_id>/product/<int:product_id>', CompanyProductDetailView.as_view(), name='company_product_update'),
    path('productcategory', ProductCategoryListView.as_view(), name='product_category_list'),
    path('company/<int:company_id>/productcategory', CompanyProductCategoryListView.as_view(), name='company_product_category_list'),
    # bill
    path('bill', BillListView.as_view(), name='bill_list'),
    path('bill/<int:bill_id>', BillDetailView.as_view(), name='bill_detail'),
    path('bill/<int:bill_id>/salesitem', SalesItemListView.as_view(), name='sales_item_list'),
    # social links
    path('company/<int:company_id>/link', SocialLinkListView.as_view(), name='company_link_list'),
    path('company/<int:company_id>/link/<int:link_id>', SocialLinkDetailView.as_view(), name='company_link_detail'),
    path('company/<int:company_id>/link/update', SocialLinkMassUpdateView.as_view(), name='company_link_mass_update'),
]