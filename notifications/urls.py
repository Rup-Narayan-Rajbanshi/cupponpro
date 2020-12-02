from django.conf.urls import url

from rest_framework import routers

from notifications.apis.notification import (
    NotificationAPI,
    DeviceAdminAPI,
    register_device,
    notification_seen, notification_unread_count
)

router = routers.SimpleRouter()
router.register(r"api/notification-user", NotificationAPI)
# router.register(r"api/devices", DeviceAdminAPI, base_name='devices')

urlpatterns = router.urls
urlpatterns += [
    url(r"^api/user-device/$", register_device, name="user-device"),
    url(r"^api/notification-seen/(?P<idx>\w+)/$", notification_seen, name="notification-seen"),
    url(r"^api/notification-unread-count/$", notification_unread_count, name="notification-unread-count")
]
