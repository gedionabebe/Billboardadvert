# Generated by Django 2.2.7 on 2020-12-15 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboards', '0004_auto_20201213_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='billboard',
            name='rate_no',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='billboard',
            name='rawrate',
            field=models.DecimalField(decimal_places=5, max_digits=30, null=True),
        ),
    ]
