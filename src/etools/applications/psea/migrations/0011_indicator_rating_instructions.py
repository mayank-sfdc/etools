# Generated by Django 2.2.4 on 2019-09-20 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psea', '0010_indicator_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='rating_instructions',
            field=models.TextField(blank=True, verbose_name='Rating Instructions'),
        ),
    ]