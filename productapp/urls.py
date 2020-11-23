# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from productapp.apis.coupon import CouponTypeListView


app_name = 'productapp'


router = routers.SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    url(r'^coupon-type/$', CouponTypeListView.as_view(), name='coupon-type-list'),
]
