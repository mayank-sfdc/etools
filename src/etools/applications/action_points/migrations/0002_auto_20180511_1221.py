# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-11 12:21
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_priority(apps, schema_editor):
    ActionPoint = apps.get_model('action_points', 'ActionPoint')
    ActionPoint.objects.filter(priority='high').update(high_priority=True)


def migrate_priority_backward(apps, schema_editor):
    ActionPoint = apps.get_model('action_points', 'ActionPoint')
    ActionPoint.objects.filter(high_priority=True).update(priority='high')


class Migration(migrations.Migration):

    dependencies = [
        ('action_points', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionpoint',
            name='high_priority',
            field=models.BooleanField(default=False, verbose_name='High Priority'),
        ),
        migrations.RunPython(migrate_priority, migrate_priority_backward),
        migrations.RemoveField(
            model_name='actionpoint',
            name='priority',
        ),
    ]
