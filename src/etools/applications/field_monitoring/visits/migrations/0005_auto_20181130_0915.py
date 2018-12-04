# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-30 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0002_auto_20181122_1525'),
        ('partners', '0029_interventionattachment_active'),
        ('field_monitoring_visits', '0004_visit_methods'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitCPOutputConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_priority', models.BooleanField(default=False, verbose_name='Priority?')),
                ('government_partners', models.ManyToManyField(blank=True, to='partners.PartnerOrganization', verbose_name='Contributing Government Partners')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field_monitoring_settings.CPOutputConfig', verbose_name='Parent')),
            ],
        ),
        migrations.RemoveField(
            model_name='visitmethodtype',
            name='cp_output',
        ),
        migrations.AlterField(
            model_name='visitmethodtype',
            name='is_recommended',
            field=models.BooleanField(default=False, verbose_name='Is Recommended'),
        ),
        migrations.AddField(
            model_name='visitcpoutputconfig',
            name='recommended_method_types',
            field=models.ManyToManyField(blank=True, related_name='cp_output_configs', to='field_monitoring_visits.VisitMethodType', verbose_name='Method(s)'),
        ),
        migrations.AddField(
            model_name='visitcpoutputconfig',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cp_output_configs', to='field_monitoring_visits.Visit', verbose_name='Visit'),
        ),
    ]