# Generated by Django 2.2.8 on 2021-03-30 05:22

from django.db import migrations, models
import helpers.app_helpers


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_deliverypartner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverypartner',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=helpers.app_helpers.content_file_name),
        ),
    ]