from django.core.management.base import BaseCommand

from notifications.helpers import trigger_fcm

class Command(BaseCommand):

    def handle(self, *args, **options):
        receivers = [
            {
                'reg_id': 956551278923,
                'title': "hello",
                'payload': {
                    "message": {
                        "en": "your message",
                    }
                }
            }
        ]
        trigger_fcm(receivers)
