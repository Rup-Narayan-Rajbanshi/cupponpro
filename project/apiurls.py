from django.urls import path, include


urlpatterns = [
    path('', include('articleapp.apiurls')),
    path('', include('bannerapp.apiurls')),
    path('', include('commonapp.apiurls')),
    path('', include('userapp.apiurls')),
    path('company/', include('company.urls')),
    path('product/', include('productapp.urls')),
    path('order/', include('orderapp.urls')),
    path('notification/', include('notifications.urls')),
    path('data_manager/', include('data_manager.urls'))
]
