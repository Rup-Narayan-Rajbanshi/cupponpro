from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from inventory.apis.stock import StockAPI
from inventory.apis.purchase import PurchaseAPI, PurchaseTransactionAPI
from inventory.apis.supplier import SupplierAPI
from inventory.apis.expense import ExpenseAPI, PaymentAPI



router = routers.SimpleRouter()
router.register(r"stock", StockAPI)
router.register(r"purchase", PurchaseAPI)
router.register(r"supplier", SupplierAPI)
router.register(r"expense", ExpenseAPI)
router.register(r"payment", PaymentAPI)
router.register(r"purchase-transaction", PurchaseTransactionAPI)


urlpatterns = router.urls