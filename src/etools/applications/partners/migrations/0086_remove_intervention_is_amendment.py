# Generated by Django 2.2.7 on 2021-06-02 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0085_auto_20210526_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='is_amendment',
        ),
    ]
