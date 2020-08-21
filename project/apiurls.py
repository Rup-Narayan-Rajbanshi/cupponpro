from django.urls import path, include


urlpatterns = [
    path('', include('articleapp.apiurls')),
    path('', include('bannerapp.apiurls')),
    path('', include('billapp.apiurls')),
    path('', include('categoryapp.apiurls')),
    path('', include('commonapp.apiurls')),
    path('', include('productapp.apiurls')),
    path('', include('userapp.apiurls')),
]
