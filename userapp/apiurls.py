# -*- coding:utf-8 -*-
from django.urls import path
from userapp.api.user import UserListView, UpdateUser

# from userapp.api.staticpage import StaticPageView

app_name = 'userapp'

urlpatterns = [
	path('users', UserListView.as_view(), name='user_list'),
	path('users/<user_id>', UpdateUser.as_view(), name='user_update'),

    ]
