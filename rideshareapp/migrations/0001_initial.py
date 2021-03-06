# Generated by Django 3.2.4 on 2021-09-01 12:23

from django.db import migrations, models
import rideshareapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fileupload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filefield', models.FileField(blank=True, default=None, upload_to=rideshareapp.models.nameFile, verbose_name='file_uploaded')),
                ('name', models.CharField(default=None, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=None, null=True)),
                ('token', models.CharField(default=None, max_length=256, null=True, unique=True)),
                ('expire_on', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, default=None, max_length=70, unique=True)),
                ('phone_number', models.CharField(default=None, max_length=256, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.IntegerField(default=None, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=None, null=True)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('is_verfied', models.BooleanField(default=False, null=True)),
                ('is_approved', models.BooleanField(default=False, null=True)),
                ('deleted_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('image', models.CharField(default='', max_length=256, null=True)),
                ('otp', models.CharField(default='', max_length=256, null=True)),
            ],
        ),
    ]
