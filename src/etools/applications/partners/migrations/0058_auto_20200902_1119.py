# Generated by Django 2.2.7 on 2020-09-02 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0057_intervention_cash_transfer_modalities'),
        ('partners', '0056_auto_20200820_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='cash_transfer_modalities',
        ),
        migrations.RenameField(
            model_name='intervention',
            old_name='cash_transfer_modalities_new',
            new_name='cash_transfer_modalities',
        )
    ]
