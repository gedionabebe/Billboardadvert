# Generated by Django 2.2.7 on 2020-01-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_account_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='password',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
