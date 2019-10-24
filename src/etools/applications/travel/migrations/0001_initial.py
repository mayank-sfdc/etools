# Generated by Django 2.2.4 on 2019-10-22 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_fsm
import etools.applications.travel.models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('action_points', '0010_actionpoint_psea_assessment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0008_auto_20190422_1537'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('activity_date', models.DateField(verbose_name='Activity Date')),
                ('activity_type', models.CharField(blank=True, choices=[('Programmatic Visit', 'Programmatic Visit'), ('Spot Check', 'Spot Check'), ('Advocacy', 'Advocacy'), ('Technical Support', 'Technical Support'), ('Meeting', 'Meeting'), ('Staff Development', 'Staff Development'), ('Staff Entitlement', 'Staff Entitlement')], default='Programmatic Visit', max_length=64, verbose_name='Activity Type')),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('reference_number', models.CharField(default=etools.applications.travel.models.generate_reference_number, max_length=15, unique=True, verbose_name='Reference Number')),
                ('status', django_fsm.FSMField(choices=[('draft', 'Draft'), ('submission', 'Submission Review'), ('submitted', 'Submitted'), ('rejected', 'Rejected'), ('approved', 'Approved'), ('review', 'Review'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', max_length=30, verbose_name='Status')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervised_itineraries', to=settings.AUTH_USER_MODEL, verbose_name='Supervisor')),
                ('traveller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to=settings.AUTH_USER_MODEL, verbose_name='Traveller')),
            ],
            options={
                'verbose_name': 'Itinerary',
                'verbose_name_plural': 'Itineraries',
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='ActivityActionPoint',
            fields=[
            ],
            options={
                'verbose_name': 'Travel Activity Action Point',
                'verbose_name_plural': 'Travel Activity Action Points',
                'abstract': False,
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('action_points.actionpoint',),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('narrative', models.TextField(blank=True, verbose_name='Narrative')),
                ('itinerary', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='travel.Itinerary', verbose_name='Itinerary')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
        migrations.CreateModel(
            name='ItineraryStatusHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submission', 'Submission Review'), ('submitted', 'Submitted'), ('rejected', 'Rejected'), ('approved', 'Approved'), ('review', 'Review'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=30)),
                ('comment', models.TextField(blank=True)),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_history', to='travel.Itinerary', verbose_name='Itinerary')),
            ],
            options={
                'verbose_name': 'Itinerary Status History',
                'verbose_name_plural': 'Itinerary Status History',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='ItineraryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('travel_method', models.CharField(blank=True, max_length=150, verbose_name='Travel Method')),
                ('destination', models.CharField(blank=True, max_length=150, verbose_name='Destination')),
                ('itinerary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='travel.Itinerary', verbose_name='Itinerary')),
            ],
            options={
                'verbose_name': 'Itinerary Item',
                'verbose_name_plural': 'Itinerary Items',
            },
        ),
        migrations.CreateModel(
            name='Involved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('involved_type', models.CharField(choices=[('section', 'Section'), ('result', 'Result'), ('intervention', 'Intervention'), ('partner', 'Partner'), ('action_point', 'Action Point'), ('monitoring', 'FM Monitoring Activity')], max_length=30, verbose_name='Type')),
                ('related_id', models.PositiveIntegerField()),
                ('activity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='involved', to='travel.Activity', verbose_name='Activity')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.Location', verbose_name='Location')),
                ('related_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Involved',
                'verbose_name_plural': 'Involved',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='itinerary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='travel.Itinerary', verbose_name='Itinerary'),
        ),
    ]
