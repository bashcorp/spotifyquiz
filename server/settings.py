"""
Django settings for spotifyquiz project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from colorlog import ColoredFormatter

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
f = open(os.path.dirname(os.path.abspath(__file__)) + "/credentials/djangokey.txt", 'r')
SECRET_KEY = f.readline()[-1]
f.close()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


TESTING_PORT = 8000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'spoton.apps.SpotOnConfig',
    'polymorphic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, '../client/spotify-quiz/build') ],
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

# HTML pages are found in the client folder, separate from the server
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, '../client/')
]


WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spoton',
        'USER': 'spoton',
        'PASSWORD': 'ImpossiblequiZ6^',
        'HOST': 'localhost',
        'TEST': {
            'NAME': 'spoton_test'
        },
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'

# Static file paths, in the client folder, separate from the server
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '../client/spotify-quiz/build/'),
    os.path.join(BASE_DIR, '../client/spotify-quiz/build/static/')
]


# Set server's log level output
if DEBUG:
    log_level = 'DEBUG'
    formatter = 'concise'
else:
    log_level = 'WARNING'
    formatter = 'verbose'

# Nicer looking logger output
log_colors = {
    'DEBUG':    'bold_black',
    'INFO':     'white',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'bold_red',
}

LOGGING = {
    'version':1,
    'disable_existing_loggers':False,
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(levelname)s %(asctime)s]\t%(message)s",
            'log_colors': log_colors,
        },
        'concise': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(levelname)s]\t%(message)s",
            'log_colors': log_colors,
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': formatter,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': log_level,
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}
