import django
django.setup()

import time
from celery import shared_task
from raven import Client

from celery.result import AsyncResult


@shared_task
def parsing(file_name):
    exec('from .parsing import {}'.format(file_name))


@shared_task
def test():
    time.sleep(60)
    return 'test success'


@shared_task
def test_parsing():
    try:
        exec('from .parsing.artSailer import *\na = ArtSailer()\na.start()')
        return 'success'
    except Exception as e:
        client = Client(
            'https://c1e68dfaf122426ab3b6edd880d08759:1237daf5ec7a47269eb5925ff8244446@sentry.io/245310')
        client.captureException()
        return str(e)
