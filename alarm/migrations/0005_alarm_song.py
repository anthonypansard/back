# Generated by Django 2.0 on 2018-05-20 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20180406_1842'),
        ('alarm', '0004_alarm_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='song',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.SET_DEFAULT, to='storage.FileSong'),
        ),
    ]
