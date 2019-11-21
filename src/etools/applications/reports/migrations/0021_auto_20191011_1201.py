# Generated by Django 2.2.4 on 2019-10-11 12:01

from django.db import connection, migrations


def copy_offices_data(apps, schema):
    OfficeOld = apps.get_model("users", "office")
    Office = apps.get_model("reports", "office")
    Country = apps.get_model("users", "country")
    if connection.tenant.schema_name != 'public':
        country = Country.objects.get(
            schema_name=connection.tenant.schema_name,
        )
        for old in OfficeOld.objects.filter(offices=country):
            Office.objects.create(
                pk=old.pk,
                name=old.name,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0020_office'),
    ]

    operations = [
        migrations.RunPython(
            copy_offices_data,
            reverse_code=migrations.RunPython.noop,
        ),
    ]