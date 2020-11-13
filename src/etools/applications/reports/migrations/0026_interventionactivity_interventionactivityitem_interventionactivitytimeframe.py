# Generated by Django 2.2.7 on 2020-07-24 08:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0025_auto_20191220_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterventionActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('context_details', models.TextField(verbose_name='Context Details')),
                ('unicef_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='UNICEF Cash')),
                ('cso_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='CSO Cash')),
                ('unicef_supplies', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='UNICEF Supplies')),
                ('cso_supplies', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='CSO Supplies')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='reports.LowerResult', verbose_name='Result')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterventionActivityTimeFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_frames', to='reports.InterventionActivity', verbose_name='Activity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterventionActivityItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('other_details', models.TextField(verbose_name='Context Details')),
                ('unicef_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='UNICEF Cash')),
                ('cso_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='CSO Cash')),
                ('unicef_suppies', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='UNICEF Supplies')),
                ('cso_supplies', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='CSO Supplies')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='reports.InterventionActivity', verbose_name='Activity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='interventionactivity',
            options={'verbose_name': 'Intervention Activity', 'verbose_name_plural': 'Intervention Activities'},
        ),
    ]