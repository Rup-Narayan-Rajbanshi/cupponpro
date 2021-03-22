# Generated by Django 2.2.8 on 2021-03-21 09:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productapp', '0006_auto_20210321_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.RegexValidator(regex='((?=.*[a-z])(?=.*[A-Z]))|((?=.*[A-Z])(?=.*[a-z]))|(?=.*[a-z])|(?=.*[A-Z])')]),
        ),
    ]
