# Generated by Django 2.2.7 on 2021-06-14 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_planning', '0009_auto_20210318_2046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monitoringactivity',
            old_name='person_responsible',
            new_name='visit_lead',
        ),
    ]
