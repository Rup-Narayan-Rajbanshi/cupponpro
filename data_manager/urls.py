from django.urls import path
from rest_framework import routers

from data_manager.apis.bulk_upload import product_data_upload, product_category_data_upload

app_name = 'data_manager'


router = routers.SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    path('upload-product-data/', product_data_upload, name='product_data_upload'),
    path('upload-product-category-data/', product_category_data_upload, name='product_category_data_upload'),

]
