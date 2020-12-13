# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from company.apis.company import FavouriteCompanyUserAPI, UserFavouriteCompanyAPI, LocalBusinessAPI


app_name = 'company'


router = routers.SimpleRouter()
router.register(r"company-fav-users", FavouriteCompanyUserAPI)
router.register(r"user-fav-companies", UserFavouriteCompanyAPI)
router.register(r"local-business", LocalBusinessAPI)

urlpatterns = router.urls

urlpatterns += [

]
