# Generated by Django 2.2.11 on 2021-02-11 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0046_auto_20200924_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerorganization',
            name='highest_risk_rating_name',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Significant', 'Significant'), ('Medium', 'Medium'), ('Low', 'Low'), ('Not Required', 'Not Required'), ('High Risk Assumed', 'High Risk Assumed'), ('Low Risk Assumed', 'Low Risk Assumed'), ('Not Assessed', 'Not Assessed')], default='', max_length=150, verbose_name='Highest Risk Rating Name'),
        ),
    ]