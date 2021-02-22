# Generated by Django 2.2.8 on 2021-02-21 11:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0039_auto_20210221_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='document/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]),
        ),
    ]