"""
WSGI config of project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os, sys

# Define settings module to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "academicspam.settings")

# Add the project and the apps to the python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath( __file__ )), '..'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath( __file__ )), '../apps'))

# Setup the django application
from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
from dj_static import Cling

application = Cling(get_wsgi_application())