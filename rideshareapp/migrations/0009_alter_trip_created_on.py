# Generated by Django 3.2.4 on 2021-09-03 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshareapp', '0008_alter_trip_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_on',
            field=models.TimeField(blank=True, default=datetime.time(9, 52, 29, 326924), null=True),
        ),
    ]
