# Generated by Django 2.2.8 on 2021-01-31 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0025_auto_20210129_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='company',
            name='zip_code',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]