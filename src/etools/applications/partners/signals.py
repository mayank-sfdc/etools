from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver

from etools.applications.partners.models import Intervention
from etools.applications.partners.tasks import sync_partner_to_prp


@receiver(post_save, sender=Intervention)
def sync_pd_partner_to_prp(instance: Intervention, created: bool, **kwargs):
    if instance.date_sent_to_partner and instance.tracker.has_changed('date_sent_to_partner'):
        sync_partner_to_prp.delay(connection.tenant.name, instance.agreement.partner_id)
