# Generated by Django 2.2.8 on 2021-03-02 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0026_merge_20210228_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlines',
            name='customer_comment',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
