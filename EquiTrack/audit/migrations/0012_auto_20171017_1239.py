# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-10-17 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0011_auto_20171017_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialAudit',
            fields=[
                ('engagement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='audit.Engagement')),
            ],
            options={
                'abstract': False,
            },
            bases=('audit.engagement',),
        ),
        migrations.CreateModel(
            name='SpecialAuditRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('audit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_recommendations', to='audit.SpecialAudit', verbose_name='Special Audit')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('finding', models.TextField()),
                ('audit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specific_procedures', to='audit.SpecialAudit', verbose_name='Special Audit')),
            ],
        ),
        migrations.AlterField(
            model_name='engagement',
            name='engagement_type',
            field=models.CharField(choices=[('audit', 'Audit'), ('ma', 'Micro Accessment'), ('sc', 'Spot Check'), ('sa', 'Special Audit')], max_length=10, verbose_name='Engagement type'),
        ),
    ]
