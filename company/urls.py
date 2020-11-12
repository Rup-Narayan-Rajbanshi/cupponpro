# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from company.apis.company import FavouriteCompanyUserAPI


app_name = 'company'


router = routers.SimpleRouter()
router.register(r"fav-company", FavouriteCompanyUserAPI)

urlpatterns = router.urls

urlpatterns += [

]
