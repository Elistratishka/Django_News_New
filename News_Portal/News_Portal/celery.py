import os
from celery import Celery
from celery.schedules import crontab
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "News_Portal.settings")
django.setup()

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'News.tasks.weekly_message',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
