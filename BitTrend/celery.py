from __future__ import absolute_import, unicode_literals
from django.conf import settings
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BitTrend.settings')
app = Celery('ManicMarket', broker=settings.BROKER_URL, result_backend=settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'order_check': {
        'task': 'BitTrend.cryptowallet.tasks.crypto_order_check_task',
        'schedule': crontab(minute="*/1"),
    }
}

app.conf.timezone = 'UTC'
