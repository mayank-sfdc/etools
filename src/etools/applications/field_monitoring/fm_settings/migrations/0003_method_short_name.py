# Generated by Django 2.2.7 on 2019-12-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0002_method_use_information_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='short_name',
            field=models.CharField(default='test', max_length=10, verbose_name='Short Name'),
            preserve_default=False,
        ),
    ]