from django.urls import path
from rest_framework import routers


app_name = 'data_manager'


router = routers.SimpleRouter()

urlpatterns = router.urls

urlpatterns += [
    path('upload-product-data/', product_data_upload, name='product_data_upload'),

]
