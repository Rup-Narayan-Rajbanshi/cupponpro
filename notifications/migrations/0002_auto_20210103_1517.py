# Generated by Django 2.2.8 on 2021-01-03 09:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveField(
            model_name='device',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='device',
            name='modified_on',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='modified_on',
        ),
        migrations.RemoveField(
            model_name='notificationcategory',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='notificationcategory',
            name='modified_on',
        ),
        migrations.AddField(
            model_name='device',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='device',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notification',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='notificationcategory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='notificationcategory',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
