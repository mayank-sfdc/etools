# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-21 10:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0004_auto_20181025_0944'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MethodType',
            new_name='FMMethodType',
        ),
    ]
