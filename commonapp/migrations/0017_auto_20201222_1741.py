# Generated by Django 2.2.8 on 2020-12-22 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0016_auto_20201222_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='image',
            field=models.ImageField(null=True, upload_to='product_category/'),
        ),
    ]