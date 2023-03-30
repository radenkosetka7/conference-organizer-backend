from __future__ import absolute_import,unicode_literals
import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pisio_backend.settings')
app = Celery('pisio_backend')
app.conf.enable_utc=False
app.conf.update(timezone='Europe/Zagreb')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'update-conference-status' :{
        'task': 'tasks.tasks.update_conference_status',
        'schedule': timedelta(minutes=60)
    },

    'update-event-status': {
        'task': 'tasks.tasks.update_event_status',
        'schedule': timedelta(minutes=60),
    },
    'update-location-status': {
        'task': 'tasks.tasks.update_occupied_status',
        'schedule':timedelta(minutes=1)
    }
}