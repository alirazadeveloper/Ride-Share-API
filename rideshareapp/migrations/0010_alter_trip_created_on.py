# Generated by Django 3.2.4 on 2021-09-03 09:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rideshareapp', '0009_alter_trip_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_on',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 9, 3, 9, 56, 49, 340906, tzinfo=utc), null=True),
        ),
    ]
