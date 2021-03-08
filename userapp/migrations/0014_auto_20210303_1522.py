# Generated by Django 2.2.8 on 2021-03-03 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0013_auto_20210303_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverificationcode',
            name='type',
            field=models.CharField(choices=[('USER_REGISTER', 'User Registration'), ('RESET_PASSWORD', 'Reset Password'), ('CHANGE_PHONE_NUMBER', 'Change Phone number'), ('SOCIAL_LOGIN', 'Social Login')], default='USER_REGISTER', max_length=20),
        ),
        migrations.AlterField(
            model_name='socialaccount',
            name='account_id',
            field=models.CharField(max_length=50),
        ),
    ]