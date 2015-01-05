"""
Django settings for theCproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@glp695%f&1&f-17g9k84$!6rbf8d52-(we_skjo06od!_up8^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
  'island.byu.edu',
]


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_mako_plus.controller',
)
CUSTOM_APPS = (
    'homepage',
    'forum',
)
INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',  # disabled beacuse our site requires login for anything useful anyway
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mako_plus.controller.router.RequestInitMiddleware',
    'lib.middleware.WebGuidMiddleware',
)

ROOT_URLCONF = 'theCproject.urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thecproject',
        'USER': 'thecproject',
        'PASSWORD': 'thecproject2014',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTH_USER_MODEL = 'homepage.SiteUser'


#################################################################
###   Debugging

DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
if DEBUG:  # development logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django_mako_plus': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'exim4_island_transport_handler': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
     }
else:  # live server logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'simple'
            },
            'exim4_island_transport_handler_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/var/log/uwsgi/app/exim4_island_transport_handler.log',
            },
        },
        'loggers': {
            'django_mako_plus': {
               'handlers': ['console'],
               'level': 'WARNING',
               'propagate': False,
            },
            'exim4_island_transport_handler': {
                'handlers': ['exim4_island_transport_handler_file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
     }



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR,  
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  


AUTHENTICATION_BACKENDS = ( 
    'django_cas_ng.backends.CASBackend',
    'django.contrib.auth.backends.ModelBackend',
)


###################################
###   Email settings

EMAIL_HOST = 'island.byu.edu'
EMAIL_PORT = 25

#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 1025


#####################################
###   CAS Authentication at BYU

CAS_SERVER_URL = 'https://cas.byu.edu/cas/login'
CAS_REDIRECT_URL = 'https://island.byu.edu/account/'
CAS_VERSION = '3'
# NOTE THAT when testing, BYU doesn't send the extended attributes.  
#CAS_SERVER_URL = 'https://cas.byu.edu/cas/login'
#CAS_REDIRECT_URL = 'http://localhost:8000/account/'



#############################################################################################
###   Specific settings for the Django-Mako-Plus app

# the default app/templates/ directory is always included in the template search path
# define any additional search directories here - this allows inheritance between apps
# absolute paths are suggested
DMP_TEMPLATES_DIRS = [ 
   os.path.join(BASE_DIR, 'homepage', 'templates'),
]

# identifies where the Mako template cache will be stored, relative to each app
DMP_TEMPLATES_CACHE_DIR = 'cached_templates'

# the default app and page to render in Mako when the url is too short
DMP_DEFAULT_PAGE = 'index'  
DMP_DEFAULT_APP = 'homepage'

# these are included in every template by default - if you put your most-used libraries here, you won't have to import them exlicitly in templates
import lib.filters
DMP_DEFAULT_TEMPLATE_IMPORTS = [
   'import os, os.path, re',
   'from decimal import Decimal',
   'from lib.filters import %s' % (','.join(lib.filters.__all__)),
]

# whether to send the custom DMP signals -- set to False for a slight speed-up in router processing
# determines whether DMP will send its custom signals during the process
DMP_SIGNALS = True

# whether to minify using rjsmin, rcssmin during 1) collection of static files, and 2) on the fly as .jsm and .cssm files are rendered
# rjsmin and rcssmin are fast enough that doing it on the fly can be done without slowing requests down
DMP_MINIFY_JS_CSS = True

###  End of settings for the base_app Controller
################################################################

