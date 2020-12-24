from django.urls import path
from rest_framework import routers

from data_manager.apis.bulk_upload import product_data_upload, product_category_data_upload
from data_manager.apis.export_qr import export_company_qr

app_name = 'data_manager'


router = routers.SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    path('upload-product/', product_data_upload, name='product_data_upload'),
    path('upload-product-category/', product_category_data_upload, name='product_category_data_upload'),
    path('export-qr/', export_company_qr, name='export-company-qr'),
]
