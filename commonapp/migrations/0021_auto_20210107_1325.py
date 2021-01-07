# Generated by Django 2.2.8 on 2021-01-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0020_auto_20201224_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW_ORDER', 'New Order'), ('CONFIRMED', 'Confirmed'), ('PROCESSING', 'Processing'), ('BILLABLE', 'Billable'), ('CANCELLED', 'Cancelled'), ('COMPLETED', 'Completed')], default='NEW_ORDER', max_length=12),
        ),
    ]