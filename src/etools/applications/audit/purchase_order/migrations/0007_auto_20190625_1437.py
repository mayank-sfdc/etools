# Generated by Django 2.2.2 on 2019-06-25 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0006_auto_20180730_1121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auditorfirm',
            options={'ordering': ('name',), 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
    ]