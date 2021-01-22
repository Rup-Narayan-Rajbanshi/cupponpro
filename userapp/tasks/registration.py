import logging
from celery.decorators import task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import time

logger = logging.getLogger('app')


@task(name="send_mail")
def send_mail(subject, msg, email, from_email=None):
    try:
        if not isinstance([], type(email)):
            email = [email]

        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        emailmessage = EmailMultiAlternatives(subject, msg, from_email, email, cc=[])
        emailmessage.send()
        logger.info("Mail successfully sent to {} for registration".format(email[0]))

    except Exception as e:
        message = "Could n't sent mail to {0} " \
                  "for registration because of {1}".format(email[0], type(e).__name__)

        logger.error(message)
        return False

    return True


@task(name="send_otp_task")
def send_otp_task(text, phone_number):
    time.sleep(1)
    try:
        from userapp.helpers import send_otp
        status = send_otp(text, phone_number)
        if status:
            logger.success(message)
            return True
        else:
            logger.error(message)
    except Exception as e:
        message = "Could not sent code to {0} " \
                  "for verification because of {1}".format(phone_number, type(e).__name__)
        logger.error(message)
    return False
