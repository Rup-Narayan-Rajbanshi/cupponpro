# Generated by Django 2.2.8 on 2020-11-20 15:16

from django.db import migrations, models
import helpers.app_helpers


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0003_auto_20201111_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo_icon',
            field=models.ImageField(blank=True, null=True, upload_to=helpers.app_helpers.content_file_name),
        ),
    ]
