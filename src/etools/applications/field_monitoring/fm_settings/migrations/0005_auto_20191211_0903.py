# Generated by Django 2.2.7 on 2019-12-11 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0004_globalconfig'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='option',
            unique_together={('question', 'value')},
        ),
    ]