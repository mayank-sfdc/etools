# Generated by Django 1.10.8 on 2018-07-16 15:47
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0013_auto_20180611_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='reference_number_year',
            field=models.IntegerField(default=2018),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agreement',
            name='special_conditions_pca',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='intervention',
            name='reference_number_year',
            field=models.IntegerField(null=True),
        ),
    ]
