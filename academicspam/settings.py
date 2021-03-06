"""Global django settings for academicspam project"""

########## IMPORTS
import os, dj_database_url#, urllib
from datetime import timedelta
########## END IMPORTS

########## DEBUG CONFIGURATION
DEBUG = TEMPLATE_DEBUG = eval(os.environ.get('DEBUG', 'False'))
########## END DEBUG CONFIGURATION

########## GENERAL CONFIGURATION
# Hosts
ALLOWED_HOSTS = ['*']

# Get the project root folder on the current computer
PROJECT_ROOT = os.path.join(os.path.dirname(\
                        os.path.abspath( __file__ )), '..')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

ROOT_URLCONF = 'academicspam.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'academicspam.wsgi.application'

# Generated using:
SECRET_KEY = os.environ.get('SECRET_KEY')

# Login urls
LOGIN_URL = '/login/'

# Honor the 'X-Forwarded-Proto' header for request.is_secure() - heroku
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
########## END GENERAL CONFIGURATION


########## DATABASE CONFIGURATION
if dj_database_url.config():
    DATABASES = {'default': dj_database_url.config()}
else:
    DATABASES = {
        'default': {
            'ENGINE':   os.environ.get('DB_ENGINE'),
            'NAME':     os.environ.get('DB_NAME'),
            'USER':     os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST':     os.environ.get('DB_HOST'),
            'PORT':     os.environ.get('DB_PORT'),
        }
    }
########## END DATABASE CONFIGURATION

########## MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## TEMPLATES CONFIGURATION
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'academicspam/templates/'),
)
########## END STATIC AND TEMPLATES CONFIGURATION


########## APPS CONFIGURATION
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'django.contrib.gis',

    # Own apps
    'spamparser',

    # Installed apps
    'django_extensions',
    'compressor',
    'storages',
    'south',
    'djcelery',
    'djkombu',
    'django_mailbox'
)
########## END APPS CONFIGURATION


########## AWS CONFIGURATION
# Get  S3 secrets
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', '')
########## END AWS CONFIGURATION


########## MEDIA FILES CONFIGURATION
# Storage class for media files
DEFAULT_FILE_STORAGE = 'academicspam.utils.s3storages.MediaRootS3BotoStorage'

# # Get S3 bucket name
AWS_STORAGE_BUCKET_NAME_MEDIA = os.environ.get('AWS_STORAGE_BUCKET_NAME_MEDIA')

# Set the url to the bucket for serving files
MEDIA_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME_MEDIA
########## END MEDIA FILES CONFIGURATION


########## STATIC FILE CONFIGURATION
# Local directory for local static collection (to track changed files)
STATIC_ROOT = os.environ.get('STATIC_ROOT', '')

if os.environ.get('AWS_STORAGE_BUCKET_NAME_STATIC'):
    # Storage class for static files and compressor
    STATICFILES_STORAGE = 'academicspam.utils.s3storages.StaticRootCachedS3BotoStorage'

    # Get S3 bucket name
    AWS_STORAGE_BUCKET_NAME_STATIC = os.environ.get(
                                        'AWS_STORAGE_BUCKET_NAME_STATIC')

    # Url prefix for all relative paths of static files
    STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME_STATIC
else:
    STATIC_URL = '/static/'

# Paths to serach for static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'academicspam/static'),
)

# List of finder classes to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)
########## END STATIC FILE CONFIGURATION


########## COMPRESSION CONFIGURATION
# Disable compression if explicity set false
if os.environ.get('COMPRESS_ENABLED', '') == 'False':
    COMPRESS_ENABLED = False

# Define the storage class for compression
if 'STATICFILES_STORAGE' in locals():
    COMPRESS_STORAGE = STATICFILES_STORAGE

# Url for retrieving compressed files
COMPRESS_URL = STATIC_URL

# Local directory for storing compressed files (needed for tracking)
COMPRESS_ROOT = STATIC_ROOT

# JS Filters
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter'
]

# CSS Filters
COMPRESS_CSS_FILTERS = [
    #creates absolute urls from relative ones
    'compressor.filters.css_default.CssAbsoluteFilter',
    #css minimizer
    'compressor.filters.cssmin.CSSMinFilter'
    ]

# Precompiler for scss
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'scss {infile} {outfile}'),
)
########## END COMPRESSION CONFIGURATION


########## CELERY CONFIGURATION
# Setup djcelery to work with db backend
import djcelery
djcelery.setup_loader()

# Set broker
BROKER_URL = 'django://'

# Set db results backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# Setup celerybeat
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Schedule periodic tasks
CELERYBEAT_SCHEDULE = {
    'read-email': {
        'task': 'spamparser.tasks.get_email',
        'schedule': timedelta(minutes=5)
    },
    'parse-email': {
        'task': 'spamparser.tasks.parse_email',
        'schedule': timedelta(minutes=5)
    }
}

# For testing tasks
CELERY_ALWAYS_EAGER = eval(os.environ.get('CELERY_ALWAYS_EAGER', 'False'))
CELERY_EAGER_PROPAGATES_EXCEPTIONS = CELERY_ALWAYS_EAGER
########## END CELERY CONFIGURATION


########## SOUTH SETTINGS
SOUTH_TESTS_MIGRATE = os.environ.get('SOUTH_TESTS_MIGRATE', True)
########## END SOUTH SETTINGS


########## LOGGING
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
########## END LOGGING


########## DEBUG Section
if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
########## END DEBUG Section
