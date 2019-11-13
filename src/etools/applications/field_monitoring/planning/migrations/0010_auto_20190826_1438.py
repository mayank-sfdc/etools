# Generated by Django 2.2.1 on 2019-08-26 14:38

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):
    dependencies = [
        ('field_monitoring_planning', '0009_auto_20190822_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoringactivity',
            name='status',
            field=django_fsm.FSMField(choices=[('draft', 'Draft'), ('checklist', 'Checklist'), ('review', 'Review'), ('assigned', 'Assigned'),
                                               ('data_collection', 'Data Collection'), ('report_finalization', 'Report Finalization'),
                                               ('submitted', 'Submitted'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft',
                                      max_length=20, verbose_name='Status'),
        ),
    ]
