# Django settings for AIVS project.
import os

BASEDIR=os.path.dirname(os.path.abspath(__file__))
ROOTDIR = os.path.abspath(os.path.join(BASEDIR, '..'))

# sloppy hack for now, override these locally in local_settings.py
LOGDIR = os.path.abspath('/home/aivs/var/logs')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Tim Gross', 'gross.timothy@gmail.com'),
)

MANAGERS = ADMINS

#DATABASES: see local_settings.py


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False # HACK: suppresses a warning on the scanner

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASEDIR, 'media/')

# URL that handles the media served from MEDIA_ROOT, with trailing slash.
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOTDIR, 'static/')

# URL prefix for static files.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/aivs/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# SECRET_KEY: see local_settings.py

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# List of absolute paths to templates that are used to override third-party apps
TEMPLATE_DIRS = (
    os.path.join(ROOTDIR, 'templates/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'aivs.urls'
APPEND_SLASH = True

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'aivs.wsgi.application'

INSTALLED_APPS = (
    'monkey_patch', # this has to be first to override the auth model
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'djcelery', # celery has to be before any of our apps
    'djcelery.transport',
    'aivs',
    'gunicorn',
    'bootstrap',
    'registration',
    'registration_backend',
    'scanner',
)

# Authentication settings
LOGIN_URL = 'login/'
LOGIN_REDIRECT_URL = 'accounts/profile/' #TODO: this is the default
LOGOUT_URL = '/'

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)


# This section has paramaters for the third-party library "django-registration"
# See local_settings for all email related settings
ACCOUNT_ACTIVATION_DAYS = 3


# This section sets up for Celery.  We're just using the database for the broker for the prototype,
# via the kombu.transport.django module.
import djcelery
djcelery.setup_loader()

BROKER_URL = 'django://'

try:
    from local_settings import *
except ImportError:
    pass

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
        },
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGDIR, 'aivs_django.log'),
            'maxBytes': '16777216', # 16 MB
            },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
       'file': {
            'handlers': ['log_file'],
            'level': 'INFO',
            }
    }
}
