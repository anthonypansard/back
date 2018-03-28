# Generated by Django 2.0 on 2018-03-28 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_auto_20180328_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileimage',
            name='GPS',
            field=models.CharField(default='', max_length=42),
        ),
        migrations.AlterField(
            model_name='fileimage',
            name='filesize',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fileimage',
            name='form',
            field=models.CharField(default='', max_length=42),
        ),
        migrations.AlterField(
            model_name='fileimage',
            name='resolution',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
