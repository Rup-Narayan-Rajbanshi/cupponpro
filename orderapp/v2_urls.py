from django.urls import path
from rest_framework import routers

from orderapp.apis.bill import BillCreateAPI, get_order_list, ManualBillCreateAPI
from orderapp.apis.order import OrderCountAPI, TableOrderAPI, TableOrderStatusAPI, CalculateOrderAPI
from orderapp.apis.order_line import OrderLineAPI, OrderLineStatusUpdateAPI
from orderapp.apis.table import TableListAPI
from orderapp.apis.voucher import VoucherListAPI

router = routers.SimpleRouter()
router.register(r"table-change-status", TableOrderStatusAPI)
router.register(r"table-order", TableOrderAPI)
router.register(r"order-line", OrderLineAPI)
router.register(r"update-order-line-status", OrderLineStatusUpdateAPI)
router.register(r"create-bill", BillCreateAPI)
router.register(r"manual-bill-create", ManualBillCreateAPI)
router.register(r"company-voucher", VoucherListAPI)

urlpatterns = router.urls

urlpatterns += {
    path('get-order-bill/<order_id>', get_order_list, name='get_order_bill'),
    path('order-count', OrderCountAPI.as_view(), name='order_count'),
    path('calculate-order', CalculateOrderAPI.as_view(), name='calculate_order'),
    path('tables', TableListAPI.as_view({'get': 'list'}), name='order_count'),
}