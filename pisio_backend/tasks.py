from datetime import timedelta

from celery import Celery
from django.conf import settings

app = Celery('pisio_backend', broker=settings.CELERY_BROKER_URL)

app.conf.beat_schedule = {
    'update-conference-status': {
        'task': 'tasks.update_conference_status',
        'schedule': timedelta(minutes=10),
    },
    'update-event-status': {
        'task': 'tasks.update_event_status',
        'schedule': timedelta(minutes=10),
    },
}