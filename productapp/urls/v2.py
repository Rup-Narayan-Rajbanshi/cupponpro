# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from productapp.apis.product_category import ProductCategoryAPI
from productapp.apis.special_food import SpecialFoodAPI


router = routers.SimpleRouter()
router.register(r"product-category", ProductCategoryAPI)
router.register(r"special-product", SpecialFoodAPI)

urlpatterns = router.urls

# urlpatterns += [
#     path('special_food', SpecialFoodAPI.as_view(), name='special_food'),
# ]
