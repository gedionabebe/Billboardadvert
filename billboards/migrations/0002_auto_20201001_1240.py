# Generated by Django 2.2.7 on 2020-10-01 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billboards', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rent',
            old_name='request',
            new_name='request_id',
        ),
    ]
