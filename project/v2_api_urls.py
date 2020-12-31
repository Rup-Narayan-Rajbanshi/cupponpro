from django.urls import path, include


urlpatterns = [
    path('order/', include('orderapp.v2_urls')),
]
