# Generated by Django 2.2.8 on 2021-02-11 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0036_auto_20210209_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commonapp.ProductCategory'),
        ),
    ]
