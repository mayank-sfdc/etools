# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-12 12:49
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publics', '0001_initial'),
        ('t2f', '0005_auto_20170112_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='new_account_currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.Currency'),
        ),
        migrations.AddField(
            model_name='expense',
            name='new_document_currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.Currency'),
        ),
        migrations.AddField(
            model_name='expense',
            name='new_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.ExpenseType'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='new_fund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.Fund'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='new_grant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.Grant'),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='new_wbs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.WBS'),
        ),
        migrations.AddField(
            model_name='iteneraryitem',
            name='new_mode_of_travel',
            field=models.CharField(choices=[('Plane', 'Plane'), ('Bus', 'Bus'), ('Car', 'Car'), ('Boat', 'Boat'), ('Rail', 'Rail')], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='new_mode_of_travel',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Plane', 'Plane'), ('Bus', 'Bus'), ('Car', 'Car'), ('Boat', 'Boat'), ('Rail', 'Rail')], max_length=5), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='travelactivity',
            name='new_travel_type',
            field=models.CharField(choices=[('Programmatic Visit', 'Programmatic Visit'), ('Spot Check', 'Spot Check'), ('Advocacy', 'Advocacy'), ('Technical Support', 'Technical Support'), ('Meeting', 'Meeting'), ('Staff Development', 'Staff Development'), ('Staff Entitlement', 'Staff Entitlement')], max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='costassignment',
            name='new_fund',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='publics.Fund'),
        ),
        migrations.AddField(
            model_name='costassignment',
            name='new_grant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='publics.Grant'),
        ),
        migrations.AddField(
            model_name='costassignment',
            name='new_wbs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='publics.WBS'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='new_currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.Currency'),
        ),
        migrations.AddField(
            model_name='iteneraryitem',
            name='new_airlines',
            field=models.ManyToManyField(related_name='_iteneraryitem_new_airlines_+', to='publics.AirlineCompany'),
        ),
        migrations.AddField(
            model_name='iteneraryitem',
            name='new_dsa_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.DSARegion'),
        ),
        migrations.AddField(
            model_name='travel',
            name='new_currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='publics.Currency'),
        ),
        migrations.AlterField(
            model_name='actionpoint',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('ongoing', 'Ongoing'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=254, null=True, verbose_name='Status'),
        ),
    ]
