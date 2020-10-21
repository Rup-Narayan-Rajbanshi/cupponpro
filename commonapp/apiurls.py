# -*- coding:utf-8 -*-
from django.urls import path
from commonapp.api.affiliate import AffiliateLinkListView, AffiliateLinkDetailView, AffiliateLinkCountView,\
    TopDiscountAffiliateListView, DealOfTheDayAffiliateListView
from commonapp.api.bill import BillListView, BillDetailView, BillVerifyView
from commonapp.api.category import CategoryListView, CategoryDetailView, SubCategoryListView, SubCategoryDetailView
from commonapp.api.company import CompanyListView, CompanyDetailView, CompanyUserListView, PartnerListView,\
    CompanyFavouriteView, ChangeCompanyEmailView, CategoryCompanyListView, CompanyCouponListView
from commonapp.api.coupon import CouponListView, CouponDetailView, CategoryCouponListView, CouponTypeListView,\
    VoucherListView, TrendingCouponListView, DealOfTheDayCouponListView
from commonapp.api.document import CompanyDocumentListView, CompanyDocumentDetailView, CompanyDocumentMassUpdateView
from commonapp.api.facility import CompanyFacilityListView, CompanyFacilityDetailView
from commonapp.api.image import CompanyImageListView, CompanyImageDetailView, CouponImageListView, CouponImageDetailView,\
    ProductImageListView, ProductImageDetailView
from commonapp.api.links import SocialLinkListView, SocialLinkDetailView, SocialLinkMassUpdateView
from commonapp.api.menu import MenuListView
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
    path('category/<uuid:category_id>', CategoryDetailView.as_view(), name='category_detail'),
    path('subcategory', SubCategoryListView.as_view(), name='subcategory_detail'),
    path('subcategory/<uuid:sub_category_id>', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    # company
	path('company', CompanyListView.as_view(), name='company_list'),
    path('company/<uuid:company_id>', CompanyDetailView.as_view(), name='company_detail'),
    path('partner', PartnerListView.as_view(), name='partner_company_list'),
    path('company/<uuid:company_id>/user', CompanyUserListView.as_view(), name='company_user_list'),
    path('company/<uuid:company_id>/favourite', CompanyFavouriteView.as_view(), name='company_favourite_list'),
    path('company/<uuid:company_id>/email', ChangeCompanyEmailView.as_view(), name='update_company_email'),
    path('category/<uuid:category_id>/company', CategoryCompanyListView.as_view(), name='category_company_list'),
    path('company/<uuid:company_id>/coupon', CompanyCouponListView.as_view(), name='company_coupon_list'),
    # company image
    path('company/<uuid:company_id>/image', CompanyImageListView.as_view(), name='company_image_list'),
    path('company/<uuid:company_id>/image/<uuid:image_id>', CompanyImageDetailView.as_view(), name='company_image_detail'),
    # document
    path('company/<uuid:company_id>/document', CompanyDocumentListView.as_view(), name='company_document_list'),
    path('company/<uuid:company_id>/document/<uuid:document_id>', CompanyDocumentDetailView.as_view(), name='company_document_detail'),
    path('company/<uuid:company_id>/document/update', CompanyDocumentMassUpdateView.as_view(), name='company_document_mass_update'),
    # coupon
    path('coupon', CouponListView.as_view(), name='coupon_list'),
    path('coupon/<uuid:coupon_id>', CouponDetailView.as_view(), name='coupon_detail'),
    path('category/<uuid:category_id>/coupon', CategoryCouponListView.as_view(), name='category_coupon_list'),
    path('coupon/type', CouponTypeListView.as_view(), name='coupon_type_list'),
    path('coupon/trending', TrendingCouponListView.as_view(), name='trending_coupon_list'),
    path('coupon/deal-of-the-day', DealOfTheDayCouponListView.as_view(), name='deal_of_the_day_coupon_list'),
    # coupon image
    path('coupon/<uuid:coupon_id>/image', CouponImageListView.as_view(), name='coupon_image_list'),
    path('coupon/<uuid:coupon_id>/image/<uuid:image_id>', CouponImageDetailView.as_view(), name='coupon_image_detail'),
    # voucher
    path('voucher', VoucherListView.as_view(), name='voucher_list'),
    # rating
    path('company/<uuid:company_id>/rating', CompanyRatingListView.as_view(), name='company_rating_list'),
    path('company/<uuid:company_id>/rating/<uuid:rating_id>', CompanyRatingDetailView.as_view(), name='company_rating_detail'),
    # facility
    path('company/<uuid:company_id>/facility', CompanyFacilityListView.as_view(), name='company_facility_list'),
    path('company/<uuid:company_id>/facility/<uuid:facility_id>', CompanyFacilityDetailView.as_view(), name='company_facility_detail'),
    # affiliate
    path('affiliate', AffiliateLinkListView.as_view(), name='affiliate_link_list'),
    path('affiliate/<uuid:affiliate_link_id>', AffiliateLinkDetailView.as_view(), name='affiliate_link_detail'),
    path('affiliate/<uuid:affiliate_link_id>/addcount', AffiliateLinkCountView.as_view(), name='affiliate_link_add_count'),
    path('affiliate/top-discount', TopDiscountAffiliateListView.as_view(), name='top_discount_affiliate_link'),
    path('affiliate/deal-of-the-day', DealOfTheDayAffiliateListView.as_view(), name='deal_of_the_day_coupon_list'),
    # search
    path('topbarsearch', TopBarSearchView.as_view(), name='top_bar_search_list'),
    # product
    path('company/<uuid:company_id>/bulkquantity', CompanyBulkQuantityListView.as_view(), name='company_bulkquantity_list'),
    path('company/<uuid:company_id>/bulkquantity/<uuid:bulk_quantity_id>', CompanyBulkQuantityDetailView.as_view(), name='company_bulkquantity_update'),
    path('company/<uuid:company_id>/product', CompanyProductListView.as_view(), name='company_product_list'),
    path('company/<uuid:company_id>/product/<uuid:product_id>', CompanyProductDetailView.as_view(), name='company_product_update'),
    path('productcategory', ProductCategoryListView.as_view(), name='product_category_list'),
    path('company/<uuid:company_id>/productcategory', CompanyProductCategoryListView.as_view(), name='company_product_category_list'),
    # product image
    path('product/<uuid:product_id>/image', ProductImageListView.as_view(), name='product_image_list'),
    path('product/<uuid:product_id>/image/<uuid:image_id>', ProductImageDetailView.as_view(), name='product_image_detail'),
    # bill
    path('bill', BillListView.as_view(), name='bill_list'),
    path('bill/<uuid:bill_id>', BillDetailView.as_view(), name='bill_detail'),
    path('bill/<uuid:bill_id>/salesitem', SalesItemListView.as_view(), name='sales_item_list'),
    path('bill/verify', BillVerifyView.as_view(), name='bill_verify'),
    # social links
    path('company/<uuid:company_id>/link', SocialLinkListView.as_view(), name='company_link_list'),
    path('company/<uuid:company_id>/link/<uuid:link_id>', SocialLinkDetailView.as_view(), name='company_link_detail'),
    path('company/<uuid:company_id>/link/update', SocialLinkMassUpdateView.as_view(), name='company_link_mass_update'),
    path('company/<uuid:company_id>/menu', MenuListView.as_view(), name='company_menu_list'),
]