# Generated by Django 2.2.8 on 2020-11-23 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0007_auto_20201121_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='paid_amount',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True),
        ),
    ]
