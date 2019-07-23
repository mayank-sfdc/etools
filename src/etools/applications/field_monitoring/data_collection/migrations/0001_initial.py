# Generated by Django 2.0.9 on 2018-12-12 08:44

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckListItemValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finding_value', models.CharField(blank=True, choices=[('y', 'As Planned'), ('n', 'Not As Planned')], max_length=1, verbose_name='Finding')),
                ('finding_description', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Checklist Item Value',
                'verbose_name_plural': 'Checklists Item Values',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='StartedMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_fsm.FSMField(choices=[('started', 'Started'), ('completed', 'Completed')], default='started', max_length=50)),
            ],
            options={
                'verbose_name': 'Started Method',
                'verbose_name_plural': 'Started Methods',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='TaskData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_probed', models.BooleanField(default=True)),
                ('started_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_data', to='field_monitoring_data_collection.StartedMethod')),
            ],
            options={
                'verbose_name': 'Task Data',
                'verbose_name_plural': 'Tasks Data',
                'ordering': ('id',),
            },
        ),
    ]