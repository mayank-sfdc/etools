from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EquiTrack.settings.production')

app = Celery('EquiTrack')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'every-monday-morning-trips': {
        'task': 'trips.tasks.process_trips',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
    },
}
