# Generated by Django 2.2.8 on 2020-12-31 04:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0002_auto_20201231_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderscanlog',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='orderscanlog',
            name='modified_on',
        ),
        migrations.AddField(
            model_name='orderscanlog',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orderscanlog',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
