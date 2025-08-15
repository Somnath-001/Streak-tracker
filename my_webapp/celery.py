# habit_tracker/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_webapp.settings')
app = Celery('my_webapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()