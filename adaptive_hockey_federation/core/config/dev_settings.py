import os

from .base_settings import *

ROOT_DIR = BASE_DIR.parent

env.read_env(ROOT_DIR / '.env')


DEV_APPS = [
    'django_extensions',
    'debug_toolbar',
]

INSTALLED_APPS += DEV_APPS

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

RESOURSES_ROOT = BASE_DIR / 'resourses'

DJANGO_SUPERUSER_USERNAME = env('DJANGO_SUPERUSER_USERNAME', default='admin')
DJANGO_SUPERUSER_EMAIL = env('DJANGO_SUPERUSER_EMAIL', default='admin@admin.ru')
DJANGO_SUPERUSER_PASSWORD = env('DJANGO_SUPERUSER_PASSWORD', default='admin')
