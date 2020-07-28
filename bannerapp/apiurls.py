# -*- coding:utf-8 -*-
from django.urls import path
from bannerapp.api.banner import BannerListView, BannerUpdateView

# from userapp.api.staticpage import StaticPageView

app_name = 'bannerapp'

urlpatterns = [
	path('banners', BannerListView.as_view(), name='banner_list'),
	path('banners/<banner_id>', BannerUpdateView.as_view(), name='banner_update'),

    ]
