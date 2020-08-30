# -*- coding:utf-8 -*-
from django.urls import path
from userapp.api.user import UserListView, UpdateUser, CreateUserView, ChangePasswordView, GeneratePasswordResetTokenView, GroupListView, ResetPasswordView, LoginView

# from userapp.api.staticpage import StaticPageView

app_name = 'userapp'

urlpatterns = [
	path('group', GroupListView.as_view(), name='group_list'),
	path('user', UserListView.as_view(), name='user_list'),
	path('user/create', CreateUserView.as_view(), name='user_create'),
	path('user/<int:user_id>', UpdateUser.as_view(), name='user_update'),
	path('user/changepassword', ChangePasswordView.as_view(), name='forgot_password'),
	path('user/forgotpassword', GeneratePasswordResetTokenView.as_view(), name='forgot_password'),
	path('user/resetpassword', ResetPasswordView.as_view(), name='reset_password'),
	path('login', LoginView.as_view(), name='user_login'),
]
