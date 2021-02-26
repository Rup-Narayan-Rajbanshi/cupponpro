# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from company.apis.company import FavouriteCompanyUserAPI, UserFavouriteCompanyAPI, LocalBusinessAPI
from company.apis.partner import PartnerAPI
from company.apis.follow import FollowAPI, GetLikeAndFollowAPI

app_name = 'company'


router = routers.SimpleRouter()
router.register(r"company-fav-users", FavouriteCompanyUserAPI)
router.register(r"user-fav-companies", UserFavouriteCompanyAPI)
router.register(r"local-business", LocalBusinessAPI)
router.register(r"partner", PartnerAPI)
router.register(r"follow", FollowAPI)
router.register(r"like-follow-check", GetLikeAndFollowAPI)

urlpatterns = router.urls

urlpatterns += [

]
