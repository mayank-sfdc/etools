# Generated by Django 2.2.20 on 2021-06-30 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0048_auto_20210506_0803'),
        ('field_monitoring_planning', '0010_auto_20210614_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringActivityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitoring_activities', models.ManyToManyField(related_name='groups', to='field_monitoring_planning.MonitoringActivity')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_activity_groups', to='partners.PartnerOrganization')),
            ],
        ),
    ]