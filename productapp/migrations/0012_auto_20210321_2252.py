# Generated by Django 2.2.8 on 2021-03-21 17:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0011_auto_20210321_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator(message='Tags must be Alphanumeric', regex='^[a-zA-Z0-9\\s,-]*$')]),
        ),
    ]
