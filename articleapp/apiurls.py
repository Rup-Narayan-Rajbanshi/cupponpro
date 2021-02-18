# -*- coding:utf-8 -*-
from django.urls import path
from articleapp.api.news import NewsArticleListView, NewsArticleDetailView
from articleapp.api.blogs import BlogAPI
from rest_framework import routers

app_name = 'articleapp'

router = routers.SimpleRouter()
router.register(r"blog", BlogAPI)

urlpatterns = router.urls

urlpatterns += [
	path('news', NewsArticleListView.as_view(), name='news_list'),
    path('news/<uuid:news_id>', NewsArticleDetailView.as_view(), name='news_detail'),
]