import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paList.settings")
app = Celery("paList")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'remove-expired-edl-entries-every-day': {
        'task': 'edl.tasks.remove_expired_edl_entries',
        'schedule': crontab(hour='*'),
        # 'schedule': crontab(hour=0, minute=0),
    },
}