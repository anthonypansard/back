# Generated by Django 2.0 on 2018-03-28 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('image', models.ImageField(upload_to='images/')),
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
                ('song', models.FileField(upload_to='songs/')),
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
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('video', models.FileField(upload_to='videos/')),
            ],
            options={
                'db_table': 'storage_filevideo',
            },
        ),
    ]
