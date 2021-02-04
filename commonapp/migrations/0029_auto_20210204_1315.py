# Generated by Django 2.2.8 on 2021-02-04 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0028_merge_20210204_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='position',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='sub_type',
            field=models.CharField(choices=[('VEG', 'VEG'), ('NON-VEG', 'NON-VEG')], default='', max_length=8, null=True),
        ),
    ]
