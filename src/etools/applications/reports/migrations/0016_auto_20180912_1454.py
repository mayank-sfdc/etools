# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-12 14:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0015_auto_20180912_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='result_type',
        ),
        migrations.DeleteModel(
            name='ResultType',
        ),
    ]