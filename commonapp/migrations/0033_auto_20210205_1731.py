# Generated by Django 2.2.8 on 2021-02-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0032_auto_20210205_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_veg',
        ),
        migrations.AddField(
            model_name='product',
            name='types',
            field=models.CharField(choices=[('VEG', 'VEG'), ('NON-VEG', 'NON-VEG')], default='', max_length=8, null=True),
        ),
    ]