# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from orderapp.apis.order import OrderStatusAPI
from orderapp.apis.order_scan_log import ValidateOrderScanAPI

app_name = 'orderapp'


router = routers.SimpleRouter()
router.register(r"change-status", OrderStatusAPI)
router.register(r"validate-qr-scan", ValidateOrderScanAPI)

urlpatterns = router.urls

# urlpatterns += [
# ]
