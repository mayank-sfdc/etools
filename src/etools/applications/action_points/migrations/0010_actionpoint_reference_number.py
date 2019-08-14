# Generated by Django 2.2.3 on 2019-08-14 11:51

from django.db import connection, migrations, models

from etools.applications.core.tests.cases import SCHEMA_NAME


def set_reference_number(apps, schema_editor):
    # Only run this when NOT in test
    if connection.tenant.schema_name != SCHEMA_NAME:
        ActionPoint = apps.get_model("action_points", "actionpoint")
        for action in ActionPoint.objects.all():
            action.reference_number = action.get_reference_number()
            action.save()


class Migration(migrations.Migration):

    dependencies = [
        ('action_points', '0009_auto_20190523_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionpoint',
            name='reference_number',
            field=models.CharField(max_length=100, null=True, verbose_name='Reference Number'),
        ),
        migrations.RunPython(set_reference_number),
    ]
