"""Celery tasks for periodic email parsing"""

from __future__ import absolute_import

from celery import shared_task

@shared_task
def hello(name='hello'):
    """Hello world test for periodic task with celery"""
    print 'Hello celerybeat'
