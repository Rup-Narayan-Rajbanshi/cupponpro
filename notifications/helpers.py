from django.conf import settings
from pyfcm import FCMNotification


def trigger_fcm(receivers):
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)
    for receiver in receivers:
        response = push_service.single_device_data_message(
            registration_id=receiver['reg_id'],
            data_message=receiver['payload']
        )
        print('receivers', receiver, response)
