# Generated by Django 2.2.5 on 2019-12-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolistapp', '0002_auto_20191205_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='interval_type',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
