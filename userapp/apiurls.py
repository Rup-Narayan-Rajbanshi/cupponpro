# -*- coding:utf-8 -*-
from django.urls import path
from userapp.api.user import UserListView, UpdateUser, ChangePasswordView, GeneratePasswordResetTokenView, ResetPasswordView

# from userapp.api.staticpage import StaticPageView

app_name = 'userapp'

urlpatterns = [
	path('users', UserListView.as_view(), name='user_list'),
	path('users/<int:user_id>', UpdateUser.as_view(), name='user_update'),
	path('users/changepassword', ChangePasswordView.as_view(), name='forgot_password'),
	path('users/forgotpassword', GeneratePasswordResetTokenView.as_view(), name='forgot_password'),
	path('users/resetpassword', ResetPasswordView.as_view(), name='reset_password'),
	

    ]
