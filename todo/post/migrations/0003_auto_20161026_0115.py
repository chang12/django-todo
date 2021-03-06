# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-25 16:15
from __future__ import unicode_literals

from django.db import migrations, models


def move_is_active_to_status(apps, schema_editor):
    Task = apps.get_model("post", "Task")
    for task in Task.objects.all():
        if not task.is_active:
            task.status = 2
        else:
            task.status = 1
        task.save()


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20161009_1643'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-priority']},
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.RunPython(move_is_active_to_status),
        migrations.RemoveField(
            model_name='task',
            name='is_active',
        ),
    ]
