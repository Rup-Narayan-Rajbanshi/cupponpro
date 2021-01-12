# Generated by Django 2.2.8 on 2021-01-12 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0007_auto_20210107_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='commonapp.Asset'),
        ),
    ]