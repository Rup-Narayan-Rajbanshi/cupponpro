# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from orderapp.apis.order import OrderStatusAPI, OrderCountAPI
from orderapp.apis.order_scan_log import ValidateOrderScanAPI
from orderapp.apis.table import TableListAPI

app_name = 'orderapp'


router = routers.SimpleRouter()
router.register(r"change-status", OrderStatusAPI)
router.register(r"validate-qr-scan", ValidateOrderScanAPI)

urlpatterns = router.urls

urlpatterns += [
    path('order-count', OrderCountAPI.as_view(), name='order_count'),
    path('tables', TableListAPI.as_view({'get': 'list'}), name='order_count'),
]
