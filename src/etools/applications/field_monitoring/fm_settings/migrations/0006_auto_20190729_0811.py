# Generated by Django 2.2.1 on 2019-07-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0005_auto_20190710_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationsite',
            name='security_detail',
        ),
        migrations.AddField(
            model_name='question',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is Active'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_custom',
            field=models.BooleanField(default=False, verbose_name='Is Custom'),
        ),
    ]
