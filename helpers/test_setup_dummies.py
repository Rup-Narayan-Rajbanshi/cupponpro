from rest_framework.authtoken.models import Token

from autho.models import User
from notifications.models import NotificationCategory
from permissions.models import Role, Permission


def set_up_owner():
    return User.objects.create_user(
        username='owner test',
        email='owner@test.com',
        password='password',
        phone_number='1234567',
        phone_number_ext='62'
    )
