# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-09-20 15:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0017_handle_null_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appliedindicator',
            old_name='cluster_id',
            new_name='cluster_indicator_id',
        ),
        migrations.AlterField(
            model_name='disaggregation',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='disaggregationvalue',
            name='disaggregation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disaggregation_values', to='reports.Disaggregation'),
        ),
        migrations.AlterField(
            model_name='disaggregationvalue',
            name='value',
            field=models.CharField(max_length=15),
        ),
    ]
