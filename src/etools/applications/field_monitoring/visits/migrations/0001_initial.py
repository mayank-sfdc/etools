# Generated by Django 2.0.9 on 2018-12-12 08:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone
import django_fsm
import etools.applications.utils.common.models.mixins
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('field_monitoring_planning', '0001_initial'),
        ('field_monitoring_shared', '0001_initial'),
        ('partners', '0029_interventionattachment_active'),
        ('field_monitoring_settings', '0002_auto_20181122_1525'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCheckListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('finding_value', models.CharField(blank=True, choices=[('y', 'As Planned'), ('n', 'Not As Planned')], max_length=1, verbose_name='Finding')),
                ('finding_description', models.TextField(blank=True, verbose_name='Description')),
                ('parent_slug', models.CharField(max_length=50, verbose_name='Parent Slug')),
                ('question_number', models.CharField(max_length=10, verbose_name='Question Number')),
                ('question_text', models.CharField(max_length=255, verbose_name='Question Text')),
                ('specific_details', models.TextField(blank=True, verbose_name='Specific Details To Probe')),
                ('methods', models.ManyToManyField(to='field_monitoring_shared.FMMethod', verbose_name='Recommended Methods')),
            ],
            options={
                'verbose_name': 'Task Checklist Item',
                'verbose_name_plural': 'Task Checklist Items',
                'ordering': ('visit_task', 'order'),
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), verbose_name='Deleted At')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('status', django_fsm.FSMField(choices=[('draft', 'Draft'), ('assigned', 'Assigned'), ('finalized', 'Finalized'), ('cancelled', 'Cancelled')], default='draft', max_length=50, verbose_name='Status')),
                ('date_assigned', model_utils.fields.MonitorField(blank=True, default=None, monitor='status', null=True, verbose_name='Date Visit Assigned', when={'assigned'})),
                ('date_finalized', model_utils.fields.MonitorField(blank=True, default=None, monitor='status', null=True, verbose_name='Date Visit Finalized', when={'finalized'})),
                ('date_cancelled', model_utils.fields.MonitorField(blank=True, default=None, monitor='status', null=True, verbose_name='Date Visit Cancelled', when={'cancelled'})),
            ],
            options={
                'verbose_name': 'Visit',
                'verbose_name_plural': 'Visits',
                'ordering': ('id',),
            },
            bases=(etools.applications.utils.common.models.mixins.InheritedModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VisitCPOutputConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_priority', models.BooleanField(default=False, verbose_name='Priority?')),
                ('government_partners', models.ManyToManyField(blank=True, to='partners.PartnerOrganization', verbose_name='Contributing Government Partners')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field_monitoring_settings.CPOutputConfig', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Visit CPOutput Config',
                'verbose_name_plural': 'Visit CPOutput Configs',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='VisitMethodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_slug', models.CharField(max_length=50, verbose_name='Parent Slug')),
                ('name', models.CharField(max_length=300, verbose_name='Name')),
                ('is_recommended', models.BooleanField(default=False, verbose_name='Is Recommended')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_types', to='field_monitoring_shared.FMMethod', verbose_name='Method')),
            ],
            options={
                'verbose_name': 'Visit Method Type',
                'verbose_name_plural': 'Visit Method Types',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='VisitTaskLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finding_value', models.CharField(blank=True, choices=[('y', 'As Planned'), ('n', 'Not As Planned')], max_length=1, verbose_name='Finding')),
                ('finding_description', models.TextField(blank=True, verbose_name='Description')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_task_links', to='field_monitoring_planning.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UNICEFVisit',
            fields=[
                ('visit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='field_monitoring_visits.Visit')),
            ],
            options={
                'verbose_name': 'UNICEF Visit',
                'verbose_name_plural': 'UNICEF Visits',
                'ordering': ('id',),
            },
            bases=('field_monitoring_visits.visit',),
        ),
        migrations.AddField(
            model_name='visittasklink',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_task_links', to='field_monitoring_visits.Visit'),
        ),
        migrations.AddField(
            model_name='visitmethodtype',
            name='visit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='method_types', to='field_monitoring_visits.Visit', verbose_name='Visit'),
        ),
        migrations.AddField(
            model_name='visitcpoutputconfig',
            name='recommended_method_types',
            field=models.ManyToManyField(blank=True, related_name='cp_output_configs', to='field_monitoring_visits.VisitMethodType', verbose_name='Method(s)'),
        ),
        migrations.AddField(
            model_name='visitcpoutputconfig',
            name='visit_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cp_output_configs', to='field_monitoring_visits.VisitTaskLink', verbose_name='Visit Task'),
        ),
        migrations.AddField(
            model_name='visit',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visit',
            name='primary_field_monitor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fm_primary_visits', to=settings.AUTH_USER_MODEL, verbose_name='Primary Field Monitor'),
        ),
        migrations.AddField(
            model_name='visit',
            name='tasks',
            field=models.ManyToManyField(related_name='visits', through='field_monitoring_visits.VisitTaskLink', to='field_monitoring_planning.Task'),
        ),
        migrations.AddField(
            model_name='visit',
            name='team_members',
            field=models.ManyToManyField(blank=True, related_name='fm_visits', to=settings.AUTH_USER_MODEL, verbose_name='Team Members'),
        ),
        migrations.AddField(
            model_name='taskchecklistitem',
            name='visit_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklist_items', to='field_monitoring_visits.VisitTaskLink', verbose_name='Task Link'),
        ),
        migrations.AlterField(
            model_name='taskchecklistitem',
            name='methods',
            field=models.ManyToManyField(related_name='checklist_items', to='field_monitoring_shared.FMMethod', verbose_name='Recommended Methods'),
        ),
    ]