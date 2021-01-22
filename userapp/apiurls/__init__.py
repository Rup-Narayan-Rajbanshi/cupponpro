from .v1 import urlpatterns, app_name
from .v2 import urlpatterns as urlpatterns_v2


urlpatterns += urlpatterns_v2
