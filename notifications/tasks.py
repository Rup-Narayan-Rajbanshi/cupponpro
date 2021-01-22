import logging
from celery.decorators import task
import time
from django.conf import settings


logger = logging.getLogger('app')


@task(name="send_fcm_task")
def send_fcm_task(receivers):
    time.sleep(1)
    try:
        from notifications.helpers import trigger_fcm
        trigger_fcm(receivers)
        return True
    except Exception as e:
        pass
    return False


@task(name="notify_company_staffs")
def notify_company_staffs(company, category, payload, asset=None, exclude_user=None):
    time.sleep(1)
    receivers = list()
    try:
        from notifications.models.notification import Notification
        receivers = Notification.send_to_company_users(
            company=company,
            category=category,
            payload=payload,
            asset=asset,
            exclude_user=exclude_user
        )
    except Exception as e:
        logger.error(str(e))
    else:
        send_fcm_task.apply_async(kwargs={'receivers': receivers})
        return True
    return False
