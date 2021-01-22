import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand

from userapp.helpers import send_otp


class Command(BaseCommand):
    def handle(self, *args, **options):
        status, message = send_otp("hello", "9849302047")
