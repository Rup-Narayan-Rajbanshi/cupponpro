# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from company.apis.company import FavouriteCompanyUserAPI, UserFavouriteCompanyAPI


app_name = 'company'


router = routers.SimpleRouter()
router.register(r"company-fav-users", FavouriteCompanyUserAPI)
router.register(r"user-fav-companies", UserFavouriteCompanyAPI)

urlpatterns = router.urls

urlpatterns += [

]
