# Generated by Django 2.2.8 on 2021-03-02 08:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import helpers.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0009_merge_20210207_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('account_type', models.CharField(choices=[('GOOGLE', 'GOOGLE'), ('FACEBOOK', 'FACEBOOK')], default='GOOGLE', max_length=10)),
                ('account_id', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex='^(\\+?[\\d]{2,3}\\-?)?[\\d]{8,10}$')])),
                ('phone_number_ext', models.CharField(default='977', max_length=6, validators=[helpers.validators.is_numeric_value])),
                ('dob', models.DateField(blank=True, null=True)),
                ('is_phone_verified', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]