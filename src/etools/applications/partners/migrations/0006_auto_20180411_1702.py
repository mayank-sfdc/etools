# Generated by Django 1.10.8 on 2018-04-11 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0005_make_not_nullable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='partner_manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='agreements_signed', to='partners.PartnerStaffMember', verbose_name='Signed by partner'),
        ),
    ]
