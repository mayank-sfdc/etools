from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from django.db import connection, models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from waffle.models import Flag, BaseModel
from waffle import managers

from users.models import Country


@python_2_unicode_compatible
class IssueCheckConfig(models.Model):
    """
    Used to enable/disable issue checks at runtime.
    """
    check_id = models.CharField(max_length=100, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {}'.format(self.check_id, self.is_active)


@python_2_unicode_compatible
class TenantFlag(models.Model):
    """
    Associate one or more countries with a Flag.
    """
    countries = models.ManyToManyField(Country, blank=True, help_text=(
        'Activate this flag for these countries.'))
    flag = models.OneToOneField(Flag)

    def __str__(self):
        return self.flag.name

    def is_active(self, request):
        "Is this flag on for this tenant, or for any other reason?"
        if getattr(request, 'tenant', None) in self.countries.all():
            return True
        return self.flag.is_active(request)


class TenantSwitchManager(managers.BaseManager):
    KEY_SETTING = 'ALL_SWITCHES_CACHE_KEY'

    def get_queryset(self):
        return super(TenantSwitchManager, self).get_queryset().prefetch_related('countries')


@python_2_unicode_compatible
class TenantSwitch(BaseModel):
    """
    Associate one or more countries with a Switch.

    'countries' is the only field we add. All other fields are copy/pasted from waffle.Switch.
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    active = models.BooleanField(default=False, help_text=(
        'Is this switch active?'))
    countries = models.ManyToManyField(Country, blank=True, help_text=(
        'Activate this switch for these countries.'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Switch is used.'))
    created = models.DateTimeField(default=timezone.now, db_index=True,
                                   help_text=('Date when this Switch was created.'))
    modified = models.DateTimeField(default=timezone.now, help_text=(
        'Date when this Switch was last modified.'))

    objects = TenantSwitchManager()

    SINGLE_CACHE_KEY = 'SWITCH_CACHE_KEY'
    ALL_CACHE_KEY = 'ALL_SWITCHES_CACHE_KEY'

    class Meta:
        verbose_name_plural = 'Switches'

    def __str__(self):
        return self.name

    def is_active(self):
        "Is this switch on for this tenant?"
        if not self.pk:
            # Nonexistent flag, return False
            return False
        if connection.tenant in self.countries.all():
            return self.active
        return False
