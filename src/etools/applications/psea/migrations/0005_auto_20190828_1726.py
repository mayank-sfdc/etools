# Generated by Django 2.2.4 on 2019-08-28 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psea', '0004_assessmentstatushistory_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessor',
            name='assessment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assessor', to='psea.Assessment', verbose_name='Assessment'),
        ),
    ]