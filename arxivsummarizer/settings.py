"""
Django settings for arxivsummarizer project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from urllib.parse import urlparse
import django_heroku
import dj_database_url



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
OPENAI_KEY = os.getenv('OPENAI_KEY')
SECRETSG = os.getenv('SECRETSG')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SECRETSG
EMAIL_USE_TLS = True
# SECURITY WARNING: don't run with debug turned on in production!
if 'ON_HEROKU' in os.environ:
    DEBUG = True#False
else:
    DEBUG = True

CSRF_TRUSTED_ORIGINS = ['https://summarizepaper.herokuapp.com','https://summarizepaper.com','https://www.summarizepaper.com','https://*.127.0.0.1']

ALLOWED_HOSTS = ['summarizepaper.herokuapp.com','summarizepaper.com','127.0.0.1']


BROKER_URL = os.environ.get("REDISCLOUD_URL", "django://")
BROKER_POOL_LIMIT = None
BROKER_CONNECTION_MAX_RETRIES = None
BROKER_TRANSPORT_OPTIONS = {
    "max_connections": 2,
}
# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'summarizer',
    'channels',
    'rosetta'
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'arxivsummarizer.backends.CustomModelBackend',
    # ...
]

ROOT_URLCONF = 'arxivsummarizer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'arxivsummarizer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('fr', _('French')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

ASGI_APPLICATION = 'arxivsummarizer.asgi.application'


# Number of messages to display per page.
ROSETTA_MESSAGES_PER_PAGE = 20
# Enable Google translation suggestions
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

YANDEX_TRANSLATE_KEY = os.getenv('YANDEX_TRANSLATE_KEY')

if 'ON_HEROKU' in os.environ:
    CHANNEL_LAYERS = {
        "default": {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [(BROKER_URL)],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                #"hosts": [(BROKER_URL)],
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }




def get_cache():
  import os
  try:
    servers = os.environ['MEMCACHIER_SERVERS']
    username = os.environ['MEMCACHIER_USERNAME']
    password = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        # TIMEOUT is not the connection timeout! It's the default expiration
        # timeout that should be applied to keys! Setting it to `None`
        # disables expiration.
        #'TIMEOUT': None,
        'TIMEOUT': 60 * 10,
        'LOCATION': servers,
        'OPTIONS': {
          'username': username,
          'password': password,
        }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60*10,
      }
    }

CACHES = get_cache()


prod_db = dj_database_url.config(conn_max_age=0)
DATABASES['default'].update(prod_db)

django_heroku.settings(locals())
