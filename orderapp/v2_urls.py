# -*- coding:utf-8 -*-
from django.urls import path
from rest_framework import routers
from orderapp.apis.order import OrderCountAPI, TableOrderAPI, TableOrderStatusAPI
from orderapp.apis.order_line import OrderLineAPI, OrderLineStatusUpdateAPI
from orderapp.apis.table import TableListAPI


router = routers.SimpleRouter()
router.register(r"table-change-status", TableOrderStatusAPI)
router.register(r"table-order", TableOrderAPI)
router.register(r"order-line", OrderLineAPI)
router.register(r"update-order-line-status", OrderLineStatusUpdateAPI)

urlpatterns = router.urls

urlpatterns += [
    path('order-count', OrderCountAPI.as_view(), name='order_count'),
    path('tables', TableListAPI.as_view({'get': 'list'}), name='order_count'),
]
