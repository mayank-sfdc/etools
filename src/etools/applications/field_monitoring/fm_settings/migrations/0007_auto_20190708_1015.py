# Generated by Django 2.2.1 on 2019-07-08 10:15

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0006_auto_20190705_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='value',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='label', verbose_name='Value'),
        ),
    ]
