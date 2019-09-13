# Generated by Django 2.2.4 on 2019-09-10 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action_points', '0010_actionpoint_psea_assessment'),
        ('psea', '0007_auto_20190906_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentActionPoint',
            fields=[
            ],
            options={
                'verbose_name': 'PSEA Assessment Action Point',
                'verbose_name_plural': 'PSEA Assessment Action Points',
                'abstract': False,
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('action_points.actionpoint',),
        ),
    ]