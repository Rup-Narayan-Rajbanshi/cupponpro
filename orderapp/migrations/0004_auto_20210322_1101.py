# Generated by Django 2.2.8 on 2021-03-22 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0003_auto_20210321_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='bill',
        ),
        migrations.AddField(
            model_name='bills',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bills', to='orderapp.Orders'),
        ),
    ]
