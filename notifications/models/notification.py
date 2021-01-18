from django.db import models, transaction

from commonapp.models.asset import Asset
from helpers.models import BaseModel
from userapp.models import User
from commonapp.models.company import CompanyUser
from jsonfield import JSONField
from rest_framework.exceptions import APIException
from notifications.exceptions import DeviceException


class Device(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_devices')
    device_type = models.CharField(
        max_length=20,
        choices=[
            ("Web", "Web"),
            ("Android", "Android"),
            ("IOS", "IOS"),
        ],
    )
    reg_id = models.CharField(max_length=512)

    @classmethod
    def update_or_create(cls, **kwargs):
        user = kwargs.get('user')
        reg_id = kwargs.get('reg_id')
        device = cls.objects.filter(user=user, reg_id=reg_id).first()
        if not device:
            return cls.objects.create(**kwargs)
        return device


# category of notification
class NotificationCategory(BaseModel):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def get_basic_info(self):
        return {"idx": self.idx, "name": self.name}

    def __str__(self):
        return self.name

    def to_representation(self, request=None):
        return {
            'id': self.id,
            'name': self.name
        }


class Notification(BaseModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='user_notifications')
    type = models.CharField(max_length=100)
    category = models.ForeignKey(NotificationCategory, on_delete=models.PROTECT)
    template = models.CharField(max_length=1000, null=True, blank=True)
    seen = models.BooleanField(default=False)
    payload = JSONField(null=True, blank=True)
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def mark_seen(self):
        self.seen = True
        self.save()
        return self

    @classmethod
    def count_unread(cls, user):
        return cls.objects.filter(user=user, seen=False).count()

    @staticmethod
    def enlist_receivers(user, payload):
        if not isinstance(user, list):
            user = [user]
        devices = Device.objects.filter(user__in=user)
        receivers = list()
        for device in devices:
            receivers.append({'reg_id': device.reg_id, 'payload': payload})
        return receivers

    @classmethod
    @transaction.atomic
    def create_notification(cls, **kwargs):
        try:
            bulk_notifications = kwargs.pop('bulk_notifications', None)
            receivers = list()
            if bulk_notifications:
                users = list()
                bulk_nots = Notification.objects.bulk_create(bulk_notifications)
                for notification in bulk_nots:
                    user = notification.user
                    payload = notification.payload
                    if user and user not in users:
                        users.append(user)
                receivers += cls.enlist_receivers(users, payload)
            else:
                category_id = kwargs.get('category', None)
                kwargs['category'] = NotificationCategory.objects.filter(id=category_id).first()
                if kwargs['category']:
                    payload = kwargs.get('payload', {})
                    if 'message' in payload:
                        message = payload.get('message', {})
                        try:
                            if not isinstance(message, dict):
                                kwargs['payload']['message'] = eval(message)
                        except Exception as e:
                            print(e, "eval failed")
                    ins = Notification.objects.create(**kwargs)
                    # send notification to user
                    user = kwargs.get('user')
                    receivers = cls.enlist_receivers(user, payload)
            return receivers
        except Exception as e:
            raise APIException(detail=str(e), code=400)

    @classmethod
    @transaction.atomic
    def send_to_company_users(cls, company, category, payload, asset=None, exclude_user=None):
        company_users = CompanyUser.objects.select_related('user').filter(company=company)
        notification_category = NotificationCategory.objects.filter(id=category).first()
        notifications = list()
        for company_user in company_users:
            user = company_user.user
            notifications.append(cls(category=notification_category,
                                     payload=payload,
                                     type='customer',
                                     user=user,
                                     asset=asset))
        receivers = cls.create_notification(bulk_notifications=notifications)
        return receivers
