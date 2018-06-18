import os
from celery import Celery, shared_task
from celery.signals import worker_init
from celery.signals import worker_shutdown
from celery.result import AsyncResult
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luna_celery.settings')

app = Celery('luna_celery', backend='amqp', broker='amqp://', include=['parsing_celery.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery -A luna worker -l info -P eventlet
# celery -A luna flower


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')


@app.task
def test(arg):
    print(arg)


@worker_init.connect
def init_worker(**kwargs):
    print('init')


@worker_shutdown.connect
def shutdown_worker(**kwargs):
    print('shut')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
