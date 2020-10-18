# -*- coding:utf-8 -*-
from django.urls import path
from articleapp.api.news import NewsArticleListView, NewsArticleDetailView

app_name = 'articleapp'

urlpatterns = [
	path('news', NewsArticleListView.as_view(), name='news_list'),
    path('news/<str:news_id>', NewsArticleDetailView.as_view(), name='news_detail'),
]