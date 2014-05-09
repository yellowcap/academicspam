"""
Celery configuration for running asynchronous and periodic tasks through celery
workers and schedulers.
"""

from __future__ import absolute_import

import os, sys

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'academicspam.settings')

# Add the project and the apps to the python path
sys.path.append(os.path.join(os.path.dirname(
                                os.path.abspath( __file__ )), '..'))
sys.path.append(os.path.join(os.path.dirname(
                                os.path.abspath( __file__ )), '../apps'))

app = Celery('academicspam')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """Task for debug mode print logs"""

    print('Request: {0!r}'.format(self.request))
