# -*- coding:utf-8 -*-
from django.urls import path
from userapp.api.user import UserListView, UpdateUser, CreateUserView,\
	CreateStaffUserView, ChangePasswordView, GeneratePasswordResetTokenView,\
	GroupListView, ResetPasswordView, CompanyGroupListView,\
	UserGroupDetailView, SignupTokenView, VerifyUserPasswordView,\
	ChangeUserEmailView, ChangeUserProfilePictureView
from userapp.api.subscription import CreateSubscription, UpdateSubscription
# from userapp.api.staticpage import StaticPageView

app_name = 'userapp'

urlpatterns = [
	# group
	path('group', GroupListView.as_view(), name='group_list'),
	path('company/group', CompanyGroupListView.as_view(), name='company_group_list'),
	path('company/<uuid:company_id>/user/<uuid:user_id>/group', UserGroupDetailView.as_view(), name="company_user_group_change"),
	# user
	path('user', UserListView.as_view(), name='user_list'),
	path('user/create', CreateUserView.as_view(), name='user_create'),
	path('user/createstaff/company/<uuid:company_id>', CreateStaffUserView.as_view(), name='staff_user_create'),
	path('user/<uuid:user_id>', UpdateUser.as_view(), name='user_update'),
	path('user/<uuid:user_id>/profile-pic', ChangeUserProfilePictureView.as_view(), name='user_profile_pic_update'),
	# email
	path('user/<uuid:user_id>/email', ChangeUserEmailView.as_view(), name='update_user_email'),
	# password
	path('user/changepassword', ChangePasswordView.as_view(), name='change_password'),
	path('user/forgotpassword', GeneratePasswordResetTokenView.as_view(), name='forgot_password'),
	path('user/resetpassword', ResetPasswordView.as_view(), name='reset_password'),
	# signup
	path('signuptoken', SignupTokenView.as_view(), name='signup_token'),
	# verify password
	path('user/password/verify', VerifyUserPasswordView.as_view(), name='verify_user_password'),
	# subscription
	path('subscription', CreateSubscription.as_view(), name='create_subscription'),
	path('subscription/<uuid:subscription_id>', UpdateSubscription.as_view(), name='update_subscription'),
]
