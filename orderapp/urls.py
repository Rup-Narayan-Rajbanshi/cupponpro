# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from orderapp.apis.order import OrderStatusAPI

app_name = 'orderapp'


router = routers.SimpleRouter()
router.register(r"change-status", OrderStatusAPI)

urlpatterns = router.urls

# urlpatterns += [
# ]
