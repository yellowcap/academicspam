"""Celery tasks for periodic email parsing"""

from __future__ import absolute_import

from celery import shared_task, task
#from scheduler.celery import celery

@task
def hello(name='hello'):
    print 'Hello celerybeat'
