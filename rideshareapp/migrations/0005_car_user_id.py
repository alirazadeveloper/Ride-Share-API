# Generated by Django 3.2.4 on 2021-09-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideshareapp', '0004_auto_20210902_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='user_id',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
