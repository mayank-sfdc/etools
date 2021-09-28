# Generated by Django 3.2.6 on 2021-09-23 15:05

from django.db import migrations, models
from django.db.models import F, OuterRef, Exists


def migrate_question_data_to_activity_child(apps, schema_editor):
    """copy question important fields to activity questions"""
    ActivityQuestion = apps.get_model('field_monitoring_data_collection', 'ActivityQuestion')
    # no way to do .update(is_hact=F(...)) because of join
    for question in ActivityQuestion.objects.select_related('question').all():
        question.is_hact = question.question.is_hact
        question.text = question.question.text
        question.save()


def cleanup_activity_groups(apps, schema_editor):
    """
    it was possible to break activity groups by changing question is_hact flag, so data should be fixed.
    remove non-hact activities from groups or remove group if not hact activities left
    partner hact values will be regenerated by system itself with update_hact_values periodic task
    """
    MonitoringActivityGroup = apps.get_model('field_monitoring_planning', 'MonitoringActivityGroup')
    ActivityQuestionOverallFinding = apps.get_model('field_monitoring_data_collection',
                                                    'ActivityQuestionOverallFinding')

    question_sq = ActivityQuestionOverallFinding.objects.filter(
        activity_question__monitoring_activity_id=OuterRef('id'),
        activity_question__is_hact=True,
        activity_question__question__level='partner',
        value__isnull=False,
    )

    for group in MonitoringActivityGroup.objects.all():
        # hact filtering code from MonitoringActivitiesQuerySet.filter_hact_for_partner
        activities_qs = group.monitoring_activities.all()
        hact_activities = list(
            activities_qs.annotate(is_hact=Exists(question_sq)).filter(status='completed', is_hact=True)
        )

        if not hact_activities:
            group.delete()

        if len(hact_activities) != activities_qs.count():
            group.set(hact_activities)


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_data_collection', '0002_auto_20191116_1045'),
        ('field_monitoring_planning', '0012_auto_20210709_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityquestion',
            name='is_hact',
            field=models.BooleanField(default=False, verbose_name='Count as HACT'),
        ),
        migrations.AddField(
            model_name='activityquestion',
            name='text',
            field=models.TextField(default='', verbose_name='Question Text'),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_question_data_to_activity_child, migrations.RunPython.noop),
        migrations.RunPython(cleanup_activity_groups, migrations.RunPython.noop),
    ]
