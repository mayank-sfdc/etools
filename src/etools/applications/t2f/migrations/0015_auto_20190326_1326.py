# Generated by Django 2.1.7 on 2019-03-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t2f', '0014_auto_20190123_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='travel',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start Date'),
        ),
    ]
