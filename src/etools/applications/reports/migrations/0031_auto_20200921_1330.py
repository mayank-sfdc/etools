# Generated by Django 2.2.7 on 2020-09-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0030_auto_20200918_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lowerresult',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Code'),
        ),
    ]
