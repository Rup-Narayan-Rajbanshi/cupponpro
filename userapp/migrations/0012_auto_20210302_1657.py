# Generated by Django 2.2.8 on 2021-03-02 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0011_auto_20210302_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialaccount',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]
