import os
from datetime import timedelta
from celery import Celery, shared_task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pisio_backend.settings')
app = Celery('pisio_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'update-conference-status': {
        'task': 'conf',
        'schedule': timedelta(seconds=10),
    },
    'update-event-status': {
        'task': 'event',
        'schedule': timedelta(minutes=10),
    },
    'update-location-status': {
        'task': 'status',
        'schedule':timedelta(minutes=30)
    }
}
