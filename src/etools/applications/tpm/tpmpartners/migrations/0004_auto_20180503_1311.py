# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-03 13:11

from django.db import migrations


def migrate_tpm_staff_members(apps, schema_editor):
    TPMPartnerStaffMember = apps.get_model('tpmpartners', 'TPMPartnerStaffMember')
    Group = apps.get_model('auth', 'Group')

    third_party_group, created = Group.objects.get_or_create(name='Third Party Monitor')
    for staff in TPMPartnerStaffMember.objects.exclude(user__groups=third_party_group):
        staff.user.groups.add(third_party_group)


class Migration(migrations.Migration):

    dependencies = [
        ('tpmpartners', '0003_tpmpartner_countries'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.RunPython(migrate_tpm_staff_members, migrations.RunPython.noop)
    ]
