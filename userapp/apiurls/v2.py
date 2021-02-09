# -*- coding:utf-8 -*-
from django.conf.urls import url
from rest_framework import routers
from django.urls import path
from userapp.api.verification import SendVerificationCodeAPI, VerifyVerificationCodeAPI, verify_otp_token
from userapp.api.registration import UserRegisterAPI
from userapp.api.customer import CustomerAPI, CustomerFromPhone

router = routers.SimpleRouter()
router.register(r"user/send-verification-code", SendVerificationCodeAPI)
router.register(r"user/verify-verification-code", VerifyVerificationCodeAPI)
router.register(r"user/register", UserRegisterAPI)
router.register(r"customer", CustomerAPI)

urlpatterns = router.urls

urlpatterns += [
    url(r"^user/verify-token/$", verify_otp_token, name="verify-token"),
    path('customer/verify', CustomerFromPhone.as_view(), name="get_customer_from_phone_number")
]
