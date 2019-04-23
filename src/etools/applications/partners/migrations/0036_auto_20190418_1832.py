# Generated by Django 2.1.7 on 2019-04-18 18:32

from django.db import connection, migrations, ProgrammingError


def rename_many_to_many_key(apps, schema_editor):

    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT sector_id FROM partners_intervention_sections')
            cursor.execute('ALTER TABLE "partners_intervention_sections" RENAME COLUMN "sector_id" TO "section_id";')
        except ProgrammingError:
            pass  # first statement will fail since is already section_id


def undo_many_to_many_key(apps, schema_editor):
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT section_id FROM partners_intervention_sections')
            cursor.execute('ALTER TABLE "partners_intervention_sections" RENAME COLUMN "section_id" TO "sector_id";')
        except ProgrammingError:
            pass  # first statement will fail since is already sector_id


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0035_auto_20190404_0858'),
    ]

    operations = [
        migrations.RunPython(rename_many_to_many_key, undo_many_to_many_key),
    ]