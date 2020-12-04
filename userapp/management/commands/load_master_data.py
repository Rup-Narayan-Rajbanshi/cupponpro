import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand

from notifications.models import NotificationCategory


class Command(BaseCommand):
    def handle(self, *args, **options):

        notification_category = NotificationCategory.objects.all()[:3]
        if notification_category.count() != 4:
            call_command('loaddata', 'notification_category')
        else:
            print('NO NEED TO LOAD NOTIFICATION CATEGORY')
