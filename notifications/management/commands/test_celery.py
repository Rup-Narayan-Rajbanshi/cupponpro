from django.core.management.base import BaseCommand

from project.celery import debug_task

class Command(BaseCommand):

    def handle(self, *args, **options):
        execute = debug_task.delay
        execute()
        # trigger_fcm(receivers)
