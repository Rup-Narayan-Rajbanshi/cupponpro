# Generated by Django 2.2.8 on 2021-01-31 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0026_auto_20210131_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='sub_type',
            field=models.CharField(choices=[('VEG', 'VEG'), ('NON-VEG', 'NON-VEG')], default='', max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='types',
            field=models.CharField(choices=[('FOOD', 'FOOD'), ('BAR', 'BAR')], default='FOOD', max_length=5),
        )
    ]