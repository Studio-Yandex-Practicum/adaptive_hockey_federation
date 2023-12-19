from .base_settings import *

ROOT_DIR = BASE_DIR.parent

env.read_env(ROOT_DIR / '.env')


DEV_APPS = [
    'django_extensions',
]

INSTALLED_APPS += DEV_APPS

DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('POSTGRES_DB', default='postgres_db'),
        'USER': env('POSTGRES_USER', default='postgres_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='postgres_password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432')
    }
}

RESOURSES_ROOT = BASE_DIR / 'resourses'

DJANGO_SUPERUSER_USERNAME = env('DJANGO_SUPERUSER_USERNAME', default='admin')
DJANGO_SUPERUSER_EMAIL = env('DJANGO_SUPERUSER_EMAIL', default='admin@admin.ru')
DJANGO_SUPERUSER_PASSWORD = env('DJANGO_SUPERUSER_PASSWORD', default='admin')
