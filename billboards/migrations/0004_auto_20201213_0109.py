# Generated by Django 2.2.7 on 2020-12-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboards', '0003_rent_advertiser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billboard',
            name='primary_photo',
            field=models.ImageField(blank=True, default='default.png', upload_to='images/'),
        ),
    ]
