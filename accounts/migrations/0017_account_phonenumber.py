# Generated by Django 2.2.7 on 2020-01-03 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200103_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='phoneNumber',
            field=models.CharField(default=None, max_length=15),
        ),
    ]