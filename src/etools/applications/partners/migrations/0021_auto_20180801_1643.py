# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-01 16:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0020_auto_20180719_1815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agreementamendment',
            options={'ordering': ('-created',)},
        ),
    ]
