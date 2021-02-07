# Generated by Django 2.2.8 on 2021-01-29 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0011_bills_is_credit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='payment_mode',
            field=models.CharField(choices=[('CARD', 'CARD'), ('CASH', 'CASH')], default=('CARD', 'CARD'), max_length=10),
        ),
    ]
