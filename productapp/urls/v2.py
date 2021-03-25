# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from productapp.apis.product_category import ProductCategoryAPI
from productapp.apis.special_food import SpecialFoodAPI
from productapp.apis.menu import MenuAPI
from productapp.apis.coupon import GlobalSearchCouponAPI, RelatedCouponCategoryAPI, SpecialCouponAPI, TagsAPI


router = routers.SimpleRouter()
router.register(r"product-category", ProductCategoryAPI)
router.register(r"special-product", SpecialFoodAPI)
router.register(r"menu", MenuAPI)
router.register(r"coupon", SpecialCouponAPI)

urlpatterns = router.urls

urlpatterns += [
    # path('special_food', SpecialFoodAPI.as_view(), name='special_food'),
    path('search-params', RelatedCouponCategoryAPI.as_view(), name='search-params'),
    path('tags', TagsAPI.as_view(), name='tags'),

]