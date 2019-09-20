# Generated by Django 2.2.1 on 2019-07-10 14:24

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_planning', '0004_auto_20190710_1424'),
        ('reports', '0017_auto_20190424_1509'),
        ('field_monitoring_visits', '0006_auto_20190710_1424'),
        ('field_monitoring_settings', '0004_cpoutputconfig_sections'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Question Category',
                'verbose_name_plural': 'Questions Categories',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Method',
                'verbose_name_plural': 'Methods',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, verbose_name='Label')),
                ('value', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='label', verbose_name='Value')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Option',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_type', models.CharField(choices=[('text', 'Text'), ('number', 'Number'), ('bool', 'Boolean'), ('choices', 'Choices')], max_length=10, verbose_name='Answer Type')),
                ('level', models.CharField(choices=[('partner', 'Partner'), ('output', 'Output'), ('intervention', 'PD/SSFA')], max_length=15, verbose_name='Level')),
                ('text', models.TextField(verbose_name='Question Text')),
                ('is_hact', models.BooleanField(default=False, verbose_name='Count as HACT')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field_monitoring_settings.Category', verbose_name='Category')),
                ('methods', models.ManyToManyField(blank=True, to='field_monitoring_settings.Method', verbose_name='Methods')),
                ('sections', models.ManyToManyField(blank=True, to='reports.Section', verbose_name='Sections')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('id',),
            },
        ),
        migrations.RemoveField(
            model_name='checklistitem',
            name='category',
        ),
        migrations.RemoveField(
            model_name='cpoutputconfig',
            name='cp_output',
        ),
        migrations.RemoveField(
            model_name='cpoutputconfig',
            name='government_partners',
        ),
        migrations.RemoveField(
            model_name='cpoutputconfig',
            name='recommended_method_types',
        ),
        migrations.RemoveField(
            model_name='cpoutputconfig',
            name='sections',
        ),
        migrations.RemoveField(
            model_name='fmmethodtype',
            name='method',
        ),
        migrations.AlterUniqueTogether(
            name='plannedchecklistitem',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='plannedchecklistitem',
            name='checklist_item',
        ),
        migrations.RemoveField(
            model_name='plannedchecklistitem',
            name='cp_output_config',
        ),
        migrations.RemoveField(
            model_name='plannedchecklistitem',
            name='methods',
        ),
        migrations.AlterUniqueTogether(
            name='plannedchecklistitempartnerinfo',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='plannedchecklistitempartnerinfo',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='plannedchecklistitempartnerinfo',
            name='planned_checklist_item',
        ),
        migrations.DeleteModel(
            name='CheckListCategory',
        ),
        migrations.DeleteModel(
            name='CheckListItem',
        ),
        migrations.DeleteModel(
            name='CPOutputConfig',
        ),
        migrations.DeleteModel(
            name='FMMethodType',
        ),
        migrations.DeleteModel(
            name='PlannedCheckListItem',
        ),
        migrations.DeleteModel(
            name='PlannedCheckListItemPartnerInfo',
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='field_monitoring_settings.Question', verbose_name='Question'),
        ),
    ]