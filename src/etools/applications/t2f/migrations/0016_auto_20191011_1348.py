# Generated by Django 2.2.4 on 2019-10-11 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0021_auto_20191011_1201'),
        ('t2f', '0015_auto_20190326_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='reports.Office', verbose_name='Office'),
        ),
    ]
