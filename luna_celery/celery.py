import os
from celery import Celery, shared_task
from celery.signals import worker_init
from celery.signals import worker_shutdown
from celery.result import AsyncResult

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luna_celery.settings')

app = Celery('luna_celery', backend='amqp', broker='guest:guest@13.125.125.118:5672//', include=['parsing_celery.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery -A luna worker -l info -P eventlet
# celery -A luna flower


@worker_init.connect
def init_worker(**kwargs):
    print('init')


@worker_shutdown.connect
def shutdown_worker(**kwargs):
    print('shut')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
