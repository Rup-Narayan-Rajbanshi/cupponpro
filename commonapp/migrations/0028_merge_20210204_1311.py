# Generated by Django 2.2.8 on 2021-02-04 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0027_company_pan_number'),
        ('commonapp', '0027_auto_20210131_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='sub_type',
            field=models.CharField(choices=[('VEG', 'VEG'), ('NON-VEG', 'NON-VEG')], default='', max_length=8, null=True),
        )
    ]
