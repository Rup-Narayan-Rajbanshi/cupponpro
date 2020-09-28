from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
    )
from rest_framework.documentation import include_docs_urls

admin.site.site_header = "Admin  @WOMCS"
admin.site.site_title = "WOMCS Admin Portal"
admin.site.index_title = "Welcome to WOMCS Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/auth/login', obtain_jwt_token),
    path('api/v1/auth/token/refresh', refresh_jwt_token),
    path('api/v1/auth/token/verify', verify_jwt_token),
    path('api/v1/', include('project.apiurls')),
    path('', include_docs_urls(title='Cupponpro API')),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
