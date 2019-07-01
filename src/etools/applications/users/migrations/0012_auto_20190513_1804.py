# Generated by Django 2.1.8 on 2019-05-13 18:04

from django.db import migrations, models
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190425_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='schema_name',
            field=models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name]),
        ),
    ]