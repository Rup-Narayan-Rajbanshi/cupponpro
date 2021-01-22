# Generated by Django 2.2.8 on 2021-01-12 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0008_auto_20210112_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlines',
            name='cooking',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderlines',
            name='new',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderlines',
            name='served',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
