from django.urls import path, include


urlpatterns = [
    path('', include('userapp.apiurls')),
    path('', include('bannerapp.apiurls')),
    path('', include('categoryapp.apiurls')),
    path('', include('commonapp.apiurls')),

]
