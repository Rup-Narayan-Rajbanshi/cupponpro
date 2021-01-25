# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from productapp.apis.product_category import ProductCategoryAPI


router = routers.SimpleRouter()
router.register(r"product-category", ProductCategoryAPI)

urlpatterns = router.urls

# urlpatterns += [
#
# ]
