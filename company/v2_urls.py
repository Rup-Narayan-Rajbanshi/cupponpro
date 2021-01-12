# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from company.apis.company import FavouriteCompanyUserAPI, UserFavouriteCompanyAPI, LocalBusinessAPI
from company.apis.partner import PartnerAPI
from company.apis.vouchers import UserVoucherListAPI

router = routers.SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    path('<company_id>/user-vouchers/', UserVoucherListAPI.as_view({'get': 'list'}), name='user_vouchers'),

]