# Generated by Django 2.0.9 on 2018-12-17 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0002_auto_20181122_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plannedchecklistitem',
            name='order',
        ),
    ]