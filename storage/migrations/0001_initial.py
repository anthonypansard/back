# Generated by Django 2.0 on 2018-04-06 16:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storage.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('filesize', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
                ('width', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(default=storage.models.now)),
                ('gps', models.CharField(blank=True, max_length=42)),
                ('extension', models.CharField(blank=True, max_length=42)),
                ('key', models.CharField(default=uuid.uuid4, max_length=42)),
                ('image', models.ImageField(blank=True, upload_to=storage.models.FileImage.upload_path_image)),
                ('thumbnail', models.ImageField(blank=True, upload_to=storage.models.FileImage.upload_path_thumbnail)),
            ],
            options={
                'db_table': 'storage_fileimage',
            },
        ),
        migrations.CreateModel(
            name='FileSong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('filesize', models.PositiveIntegerField(default=0)),
                ('height', models.PositiveIntegerField(default=0)),
                ('width', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(default=storage.models.now)),
                ('extension', models.CharField(blank=True, max_length=42)),
                ('length', models.DurationField(default=datetime.timedelta(0))),
                ('key', models.CharField(default=storage.models.FileSong.get_uuid, max_length=42)),
                ('song', models.FileField(blank=True, upload_to=storage.models.FileSong.upload_path)),
                ('thumbnail', models.ImageField(blank=True, upload_to=storage.models.FileSong.upload_path_thumbnail)),
            ],
            options={
                'db_table': 'storage_filesong',
            },
        ),
        migrations.CreateModel(
            name='FileUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('right', models.CharField(max_length=42)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'storage_fileuser',
            },
        ),
        migrations.CreateModel(
            name='FileVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=42)),
                ('filesize', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(default=storage.models.now)),
                ('extension', models.CharField(blank=True, max_length=42)),
                ('length', models.DurationField(default=datetime.timedelta(0))),
                ('album', models.CharField(blank=True, max_length=42)),
                ('artist', models.CharField(blank=True, max_length=42)),
                ('key', models.CharField(default=storage.models.FileVideo.get_uuid, max_length=42)),
                ('video', models.FileField(blank=True, upload_to=storage.models.FileVideo.upload_path)),
                ('thumbnail', models.ImageField(blank=True, upload_to=storage.models.FileVideo.upload_path_thumbnail)),
            ],
            options={
                'db_table': 'storage_filevideo',
            },
        ),
    ]
