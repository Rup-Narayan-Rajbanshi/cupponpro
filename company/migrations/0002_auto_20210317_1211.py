# Generated by Django 2.2.8 on 2021-03-17 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commonapp', '0002_auto_20210317_1211'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follows',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AddField(
            model_name='follows',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favouritecompany',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AddField(
            model_name='favouritecompany',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AddField(
            model_name='document',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company'),
        ),
        migrations.AddField(
            model_name='companyuser',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company'),
        ),
        migrations.AddField(
            model_name='companyuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='company_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company_category', to='commonapp.Category'),
        ),
        migrations.AddField(
            model_name='company',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='commonapp.SubCategory'),
        ),
        migrations.AddField(
            model_name='asset',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company'),
        ),
    ]
