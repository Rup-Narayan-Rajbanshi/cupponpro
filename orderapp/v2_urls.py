from django.urls import path
from rest_framework import routers

from orderapp.apis.bill import BillCreateAPI, get_order_list, ManualBillCreateAPI, BillAPI, BIllUpdateAPI
from orderapp.apis.order import OrderCountAPI, TableOrderAPI, TableOrderStatusAPI, CalculateOrderAPI, UserOrderListAPI, \
    CustomerOrderAPI, MasterQROrderAPI, latest_asset_order, TableOrderOrderlineUpdateAPI
from orderapp.apis.order_line import OrderLineAPI, OrderLineStatusUpdateAPI
from orderapp.apis.table import AssetListAPI
from orderapp.apis.voucher import VoucherListAPI, CustomerVoucherAPI
from orderapp.apis.sales import GetSellItemReportAPI, TableSalesAPI, GetServiceChargeAPI, GetSellReport, CreditReportAPI
from orderapp.apis.transaction import BillTransactionHistoryAPI
from orderapp.apis.coupon import SpecialCouponAPI

router = routers.SimpleRouter()
router.register(r"table-change-status", TableOrderStatusAPI)
router.register(r"table-order", TableOrderAPI)
router.register(r"(?P<company_id>[0-9a-f-]+|)/customer-order", CustomerOrderAPI)
router.register(r"(?P<company_id>[0-9a-f-]+|)/master-qr-order", MasterQROrderAPI)
router.register(r"order-line", OrderLineAPI)
router.register(r"update-order-line-status", OrderLineStatusUpdateAPI)
router.register(r"create-bill", BillCreateAPI)
router.register(r"bill", BillAPI)
router.register(r"manual-bill-create", ManualBillCreateAPI)
router.register(r"company-voucher", VoucherListAPI)
router.register(r"assets", AssetListAPI)
router.register(r"customer-vouchers", CustomerVoucherAPI)
router.register(r"update-bill", BIllUpdateAPI)
router.register(r"transaction-history", BillTransactionHistoryAPI)
router.register(r"update-line-status", TableOrderOrderlineUpdateAPI)

router.register(r"coupon", SpecialCouponAPI)


urlpatterns = router.urls

urlpatterns += {
    path('get-order-bill/<order_id>', get_order_list, name='get_order_bill'),
    path('latest-asset-order/<asset_id>', latest_asset_order, name='latest_asset_order'),
    path('order-count', OrderCountAPI.as_view(), name='order_count'),
    path('calculate-order', CalculateOrderAPI.as_view(), name='calculate_order'),
    path('user-orders', UserOrderListAPI.as_view({'get': 'list'}), name='user_orders'),
    path('sell-item-report/', GetSellItemReportAPI.as_view(), name='sell_item_report'),
    path('table-sales', TableSalesAPI.as_view(), name='table-sales'),
    path('service-charge-report/', GetServiceChargeAPI.as_view(), name='service-charge-report'),
    path('sell-report/', GetSellReport.as_view(), name='service-charge-report'),
    path('credit-report/', CreditReportAPI.as_view(), name='credit-report')

}
