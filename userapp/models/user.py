import re
from rest_framework.response import Response
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.dispatch import receiver



class UserManager(BaseUserManager):
    def create_user(self, first_name, middle_name, last_name, email, phone_number,\
        password=None, is_active=False, is_staff=False, is_admin=False):
        if not first_name:
            raise ValueError(_("User must have a First name."))

        if not last_name:
            raise ValueError(_("User must have a Last name."))

        if not email:
            raise ValueError(_("Users must have email address."))

        if not phone_number:
            raise ValueError(_("Users must have Phone Number."))

        if not password:
            raise ValueError(_("User must have a password."))

        user_obj = self.model(
            email=email
        )
        user_obj.first_name = first_name
        user_obj.middle_name = middle_name
        user_obj.last_name = last_name
        user_obj.phone_number = phone_number
        user_obj.password = password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, first_name, middle_name, last_name, email,\
        phone_number, password=None):
        self.create_user(first_name, middle_name, last_name,\
            email, phone_number, password, is_staff=False, is_admin=False, is_active=True)

    def create_superuser(self, first_name, middle_name, last_name, email,\
        phone_number, password=None):
        user = self.create_user(first_name, middle_name, last_name,\
            email, phone_number, password, is_staff=True, is_admin=True, is_active=True)


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=50,\
        validators=[RegexValidator(
            regex="((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])"
            )])
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50,\
        validators=[RegexValidator(
            regex="((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])"
            )],)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='profile/', blank=False, null=True,\
        default='profile/default.png')
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now=True)
    update_password = True
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'middle_name',\
        'last_name', 'phone_number']

    objects = UserManager()

    class Meta:
        db_table = 'user'


    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        text_email = str(self.email)
        self.username = text_email.split('@')[0]
        if (self.admin != 'True' and self.update_password):
            self.set_password(self.password)
        elif(self.admin == 'True' and self.update_password == True):
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def full_name(self):
        return "%s %s" %(self.first_name,self.last_name)
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
