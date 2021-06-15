# Generated by Django 2.2.20 on 2021-05-06 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0025_auto_20191220_2022'),
        ('partners', '0047_auto_20210211_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerorganization',
            name='lead_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.Office', verbose_name='Lead Office'),
        ),
        migrations.AddField(
            model_name='partnerorganization',
            name='lead_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reports.Section', verbose_name='Lead Section'),
        ),
    ]