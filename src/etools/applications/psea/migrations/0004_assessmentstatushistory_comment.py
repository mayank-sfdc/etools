# Generated by Django 2.2.4 on 2019-08-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psea', '0003_auto_20190826_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentstatushistory',
            name='comment',
            field=models.TextField(blank=True),
        ),
    ]