# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from productapp.apis.product_category import ProductCategoryAPI
from productapp.apis.special_food import SpecialFoodAPI
from productapp.apis.menu import MenuAPI


router = routers.SimpleRouter()
router.register(r"product-category", ProductCategoryAPI)
router.register(r"special-product", SpecialFoodAPI)
router.register(r"menu", MenuAPI)

urlpatterns = router.urls

# urlpatterns += [
#     path('special_food', SpecialFoodAPI.as_view(), name='special_food'),
# ]
