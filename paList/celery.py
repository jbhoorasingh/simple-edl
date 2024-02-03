import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paList.settings")
app = Celery("paList")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()