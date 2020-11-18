import os
import shortuuid
import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from project.settings.base import EMAIL_HOST_USER
from commonapp.models.address import Address
from helpers.app_helpers import url_builder

class UserManager(BaseUserManager):
    def _create_user(self, first_name, middle_name, last_name, email, phone_number,\
        password, is_active=True, is_staff=False, is_admin=False):
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
            email=email.lower()
        )
        user_obj.first_name = first_name
        user_obj.middle_name = middle_name
        user_obj.last_name = last_name
        user_obj.phone_number = phone_number
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, first_name, middle_name, last_name, email,\
        phone_number, password=None):
        return self._create_user(first_name, middle_name, last_name,\
            email, phone_number, password)

    def create_superuser(self, first_name, middle_name, last_name, email,\
        phone_number, password=None):
        user = self._create_user(first_name, middle_name, last_name,\
            email, phone_number, password, is_staff=True, is_admin=True)
        # assign admin as group
        user_group, _ = Group.objects.get_or_create(name='user')
        admin_group, _ = Group.objects.get_or_create(name='admin')
        user.group.add(user_group, admin_group)
        user.save()
        return user


class User(AbstractBaseUser, Address):
    # Gender Choices Variables
    Male = 'M'
    Female = 'F'
    Other = 'O'
    GENDER = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    first_name = models.CharField(max_length=50,\
        validators=[RegexValidator(
            regex="((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])"
            )])
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50,\
        validators=[RegexValidator(
            regex="((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])"
            )],)
    gender = models.CharField(max_length=6, choices=GENDER, default=Male, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True,\
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    image = models.ImageField(upload_to='profile/', blank=False, null=True,\
        default='profile/default.png')
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    dob = models.DateField(null=True, blank=True)
    group = models.ManyToManyField(Group)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'middle_name',\
        'last_name', 'phone_number']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def to_representation(self, request=None):
        if self:
            image = url_builder(self.image, request)
            return {
                "id": self.id,
                "first_name": self.first_name,
                "middle_name": self.middle_name,
                "last_name": self.last_name,
                "image": image,
                "email": self.email
            }
        return None

    @property
    def full_name(self):
        return "%s %s" %(self.first_name, self.last_name)

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

@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            if not 'default.png' in str(instance.image.path):
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
    except:
        return False

    new_file = instance.image
    if old_file:
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                if not 'default.png' in str(old_file.path):
                    os.remove(old_file.path)

class PasswordResetToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=6, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_token'
        verbose_name_plural = "password reset tokens"
        ordering = ['-created_at']

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        ''' On save, generate token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=6)
        return super(PasswordResetToken, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=PasswordResetToken)
def auto_send_passoword_reset_token_email(sender, instance, **kwargs):
    """
    Send email with the password reset token
    """
    if not instance.pk:
        return False

    try:
        if not instance.is_used:
            user = User.objects.get(id=instance.user.id)
            token = PasswordResetToken.objects.get(id=instance.pk).token
            user_name = user.full_name
            user_email = user.email
            subject = 'Password Reset Token'

            text_template = get_template('email/passwordResetTokenEmail.txt')
            html_template = get_template('email/passwordResetTokenEmail.html')
            context = {
                'subject': subject,
                'user_name': user_name,
                'user_email': user_email,
                'token': token,
                'domain_name': 'http://127.0.0.1:8000'
            }
            text_content = text_template.render(context)
            html_content = html_template.render(context)
            email_from = EMAIL_HOST_USER

            mail = EmailMultiAlternatives(subject, text_content, email_from, [user_email])
            mail.attach_alternative(html_content, "text/html")
            mail.send()

    except sender.DoesNotExist:
        return False

class LoginToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'login_token'
        ordering = ['-created_at']

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        ''' On save, generate token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=4)
        return super(LoginToken, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=LoginToken)
def auto_send_login_token_email(sender, instance, **kwargs):
    """
    Send email with the login token
    """
    if not instance.pk:
        return False

    try:
        if not instance.is_used:
            user = User.objects.get(id=instance.user.id)
            token = LoginToken.objects.get(id=instance.pk).token
            user_name = user.full_name
            user_email = user.email
            subject = 'Login Token'

            text_template = get_template('email/loginTokenEmail.txt')
            html_template = get_template('email/loginTokenEmail.html')
            context = {
                'subject': subject,
                'user_name': user_name,
                'user_email': user_email,
                'token': token,
                'domain_name': 'http://127.0.0.1:8000'
            }
            text_content = text_template.render(context)
            html_content = html_template.render(context)
            email_from = EMAIL_HOST_USER

            mail = EmailMultiAlternatives(subject, text_content, email_from, [user_email])
            mail.attach_alternative(html_content, "text/html")
            mail.send()

    except sender.DoesNotExist:
        return False

class SignupToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=True)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=15,\
        validators=[RegexValidator(regex=r"^(\+?[\d]{2,3}\-?)?[\d]{8,10}$")])
    token = models.CharField(max_length=4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'signup_token'
        ordering = ['-created_at']

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        ''' On save, generate token '''
        if not self.token:
            self.token = shortuuid.ShortUUID().random(length=4)
        return super(SignupToken, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=SignupToken)
def auto_send_signup_token_email(sender, instance, **kwargs):
    """
    Send email with the signup token
    """
    if not instance.pk:
        return False

    try:
        if not instance.is_used:
            token_obj = SignupToken.objects.get(id=instance.pk)
            token = token_obj.token
            user_email = token_obj.email
            subject = 'Signup Token'

            text_template = get_template('email/signupTokenEmail.txt')
            html_template = get_template('email/signupTokenEmail.html')
            context = {
                'subject': subject,
                'user_email': user_email,
                'token': token,
                'domain_name': 'http://127.0.0.1:8000'
            }
            text_content = text_template.render(context)
            html_content = html_template.render(context)
            email_from = EMAIL_HOST_USER

            mail = EmailMultiAlternatives(subject, text_content, email_from, [user_email])
            mail.attach_alternative(html_content, "text/html")
            mail.send()

    except sender.DoesNotExist:
        return False
