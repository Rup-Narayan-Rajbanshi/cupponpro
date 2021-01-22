# Generated by Django 2.2.8 on 2021-01-02 13:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0020_auto_20201224_1824'),
        ('orderapp', '0003_auto_20201231_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('payment_mode', models.CharField(choices=[('CARD', 'CARD'), ('CASH', 'CASH')], default='CASH', max_length=10)),
                ('service_charge', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('tax', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('invoice_number', models.CharField(editable=False, max_length=8)),
                ('is_manual', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='commonapp.Company')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='orders',
            name='bill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orderapp.Bills'),
        ),
    ]
