# Generated by Django 3.2.4 on 2021-09-03 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshareapp', '0007_auto_20210903_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='created_on',
            field=models.TimeField(blank=True, default=datetime.time(9, 46, 29, 659415), null=True),
        ),
    ]
