import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand

from django.contrib.auth.models import Group
from notifications.models import NotificationCategory


class Command(BaseCommand):
    def handle(self, *args, **options):

        notification_category = NotificationCategory.objects.all()
        if notification_category.count() != 4:
            call_command('loaddata', 'notification_category')
        else:
            print('NO NEED TO LOAD NOTIFICATION CATEGORY')

        groups = Group.objects.count()
        if groups != 5:
            # new_groups = [
            #     Group(name='admin'),
            #     Group(name='owner'),
            #     Group(name='manager'),
            #     Group(name='sales'),
            #     Group(name='user')
            # ]
            # Group.objects.bulk_create(new_groups)
            new_groups = ['admin', 'owner', 'manager', 'sales', 'user']
            for group in new_groups:
                g, _ = Group.objects.get_or_create(name=group)
            print("GROUP LOADED")
        else:
            print('NO NEED TO LOAD GROUP')
