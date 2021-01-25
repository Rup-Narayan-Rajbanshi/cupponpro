from django.urls import path, include


urlpatterns = [
    path('order/', include('orderapp.v2_urls')),
    path('company/', include('company.v2_urls')),
    path('product/', include('productapp.urls.v2'))
]
