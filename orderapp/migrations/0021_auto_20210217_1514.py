# Generated by Django 2.2.8 on 2021-02-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0020_auto_20210217_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills',
            name='is_service_charge',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='is_service_charge',
            field=models.BooleanField(default=True),
        ),
    ]
