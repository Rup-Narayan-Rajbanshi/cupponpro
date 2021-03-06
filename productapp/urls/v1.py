# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from productapp.apis.coupon import CouponTypeListView
from productapp.apis.product_image import CompanyProductImageAPI
from productapp.apis.coupon import DealOfDayAPI, TrendingCouponAPI, RecentCouponAPI, LocalBusinessCouponAPI


# app_name = 'productapp'


router = routers.SimpleRouter()
router.register(r"image", CompanyProductImageAPI)
router.register(r"deal-of-day", DealOfDayAPI)
router.register(r"trending-coupon", TrendingCouponAPI)
router.register(r"recent-coupon", RecentCouponAPI)
router.register(r"local-business-coupon", LocalBusinessCouponAPI)

urlpatterns = router.urls

urlpatterns += [
    url(r'^coupon-type/$', CouponTypeListView.as_view(), name='coupon-type-list')
]
