# Generated by Django 2.2.8 on 2021-02-21 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0038_auto_20210212_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='print_order',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='print_tax_invoice',
            field=models.BooleanField(default=True),
        ),
    ]