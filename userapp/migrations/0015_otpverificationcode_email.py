# Generated by Django 2.2.8 on 2021-03-05 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0014_auto_20210303_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='otpverificationcode',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
    ]