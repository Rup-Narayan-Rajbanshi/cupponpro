from django.conf.urls import url

from rest_framework import routers

from notifications.apis.alert_push_notification import send_table_alert_notification
from notifications.apis.notification import (
    NotificationAPI,
    register_device,
    notification_seen, notification_unread_count,
    AssetNotificationAPI)

router = routers.SimpleRouter()
router.register(r"notification-user", NotificationAPI)
router.register(r"(?P<asset_id>[0-9a-f-]+|)/asset-notifications", AssetNotificationAPI)
# router.register(r"api/devices", DeviceAdminAPI, base_name='devices')

urlpatterns = router.urls
urlpatterns += [
    url(r"^user-device/$", register_device, name="user-device"),
    url(r"^mark-seen/?(?P<notification_id>[0-9a-f-]+|)/$", notification_seen, name="mark-seen"),
    url(r"^bulk-mark-seen/$", notification_seen, name="mark-seen"),
    # url(r"^mark-seen/<uuid:user_id>\w+/$", notification_seen, name="mark-seen"),
    url(r"^unread-count/$", notification_unread_count, name="unread-count"),
    url(r"^send-table-alert-notification/?(?P<asset_id>[0-9a-f-]+|)/$", send_table_alert_notification, name="send_table_alert_notification")
]
