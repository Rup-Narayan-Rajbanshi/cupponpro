# Generated by Django 2.2.8 on 2021-03-21 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0002_auto_20210317_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='payable_amount',
            field=models.DecimalField(blank=True, decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='orders',
            name='service_charge',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
