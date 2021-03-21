from django.urls import path, include
from productapp.apis.coupon import GlobalSearchCouponAPI


urlpatterns = [
    path('order/', include('orderapp.v2_urls')),
    path('company/', include('company.v2_urls')),
    path('product/', include('productapp.urls.v2')),
    path('inventory/', include('inventory.urls')),

    path('search', GlobalSearchCouponAPI.as_view({'get': 'list'}), name='search'),
]
