# Generated by Django 3.2.6 on 2022-01-20 13:49
import logging

from django.db import migrations, models
import django.db.models.deletion


logger = logging.getLogger(__name__)


def migrate_groups_to_realmgroups(apps, schema_editor):
    """creates realms and migrates the user groups to realm groups"""
    User = apps.get_model('users', 'User')
    Realm = apps.get_model('users', 'Realm')
    RealmGroup = Realm.groups.through
    BusinessArea = apps.get_model('publics', 'BusinessArea')

    for user in User.objects.select_related(
            'profile', 'profile__country').prefetch_related('groups',).all():
        user_groups_ids = user.groups.values_list('pk', flat=True)
        if not user_groups_ids:
            continue
        business_area = None
        vendor_number = user.profile.vendor_number
        if hasattr(user.profile, 'country') and user.profile.country:
            b_a_code = user.profile.country.business_area_code
            try:
                business_area = BusinessArea.admin_objects.get(code=b_a_code)
            except BusinessArea.DoesNotExist:
                logger.error(f'Not Business Area found for code {b_a_code}')
                logger.error(f'Could not migrate groups for user {user.id} on country '
                             f'{getattr(user, "country", "N/A")}')
                continue
        unique_realm_name = f"{business_area.name if business_area else '-'}/" \
                            f"{vendor_number if vendor_number else '-'}" \
                            f"({', '.join(map(lambda x: str(x), user_groups_ids))})"
        logger.info(f'Realm name {unique_realm_name}')
        realm, _created = Realm.objects.get_or_create(
            name=unique_realm_name,
            business_area=business_area,
            vendor_number=vendor_number)
        realm_groups = [RealmGroup(realm_id=realm.pk, group_id=group_id) for group_id in user_groups_ids]
        if _created:
            logger.info(f'New realm created id: {realm.pk}')
            realm.groups.through.objects.bulk_create(realm_groups)
            user.realms.add(realm)
        else:
            logger.info(f'User groups ids {user_groups_ids}')
            logger.info(f'Realm groups ids {realm.groups.values_list("pk", flat=True)}')
            if set(user_groups_ids) == set(realm.groups.values_list('pk', flat=True)):
                logger.info(f'Reusing realm with id {realm.id}')
                user.realms.add(realm)
            else:
                logger.info('Creating new realm for different groups')
                new_realm = Realm.objects.create(
                    name=unique_realm_name,
                    business_area=business_area, vendor_number=vendor_number)
                realm_groups = [
                    RealmGroup(
                        realm_id=new_realm.pk,
                        group_id=group_id) for group_id in user_groups_ids]

                new_realm.groups.through.objects.bulk_create(realm_groups)
                user.realms.add(realm)


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('publics', '0006_auto_20190625_1547'),
        ('users', '0016_country_custom_dashboards'),
    ]

    operations = [
        migrations.CreateModel(
            name='Realm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Realm Name')),
                ('vendor_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Vendor Number')),
                ('business_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='realms', to='publics.businessarea', verbose_name='Business Area')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups available in the user realm. A user will get all permissions granted to each of the realm groups.', related_name='realm_set', related_query_name='realm', to='auth.Group', verbose_name='groups')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='realms',
            field=models.ManyToManyField(blank=True, help_text='The realm this user belongs to. A user will get all permissions granted to each of the realm groups.', related_name='user_set', related_query_name='user', to='users.Realm', verbose_name='Realms'),
        ),
        migrations.RunPython(migrate_groups_to_realmgroups, migrations.RunPython.noop)
    ]