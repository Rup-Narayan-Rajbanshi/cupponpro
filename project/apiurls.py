from django.urls import path, include


urlpatterns = [
    path('', include('articleapp.apiurls')),
    path('', include('bannerapp.apiurls')),
    path('', include('commonapp.apiurls')),
    path('', include('userapp.apiurls')),
    path('', include('company.apiurls'))
]
