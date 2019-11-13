# Generated by Django 2.2.1 on 2019-08-09 14:38

from django.db import migrations, models
import django.db.models.deletion


def cleanup(apps, schema_editor):
    Finding = apps.get_model('field_monitoring_data_collection', 'Finding')
    Finding.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_data_collection', '0006_auto_20190730_1132'),
    ]

    operations = [
        migrations.RunPython(cleanup, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='finding',
            name='activity_question',
        ),
        migrations.AddField(
            model_name='finding',
            name='activity_question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='findings',
                                    to='field_monitoring_data_collection.ActivityQuestion', verbose_name='Activity Question'),
            preserve_default=False,
        ),
    ]
