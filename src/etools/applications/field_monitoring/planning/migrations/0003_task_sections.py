# Generated by Django 2.0.9 on 2018-12-27 08:47

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):
    dependencies = [
        ('reports', '0013_auto_20180709_1348'),
        ('field_monitoring_planning', '0002_yearplan_other_aspects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='plan_by_month',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(blank=True, default=0), blank=True, default=[],
                                                            size=None, verbose_name='Plan By Month'),
        ),
        migrations.AddField(
            model_name='task',
            name='sections',
            field=models.ManyToManyField(to='reports.Section', verbose_name='Sections'),
        ),
    ]
