# Generated by Django 2.1.7 on 2019-03-26 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flaggedissue',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='FlaggedIssue',
        ),
    ]
