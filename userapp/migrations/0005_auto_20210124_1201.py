# Generated by Django 2.2.8 on 2021-01-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_auto_20210124_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(default='address', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(default='city', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(default='country', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.CharField(default='state', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.CharField(default=123, max_length=30),
            preserve_default=False,
        ),
    ]