from django.conf.urls import url

from rest_framework import routers

from notifications.apis.notification import (
    NotificationAPI,
    DeviceAdminAPI,
    register_device,
    notification_seen, notification_unread_count
)

router = routers.SimpleRouter()
router.register(r"notification-user", NotificationAPI)
# router.register(r"api/devices", DeviceAdminAPI, base_name='devices')

urlpatterns = router.urls
urlpatterns += [
    url(r"^user-device/$", register_device, name="user-device"),
    url(r"^mark-seen/?(?P<notification_id>[0-9a-f-]+|)/$", notification_seen, name="mark-seen"),
    # url(r"^mark-seen/<uuid:user_id>\w+/$", notification_seen, name="mark-seen"),
    url(r"^unread-count/$", notification_unread_count, name="unread-count")
]
