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
        'ENGINE': env('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('POSTGRES_DB', default='postgres_db'),
        'USER': env('POSTGRES_USER', default='postgres_user'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='postgres_password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432')
    }
}

DJANGO_SUPERUSER_USERNAME = env('DJANGO_SUPERUSER_USERNAME', default='admin')
DJANGO_SUPERUSER_EMAIL = env('DJANGO_SUPERUSER_EMAIL', default='admin@admin.ru')
DJANGO_SUPERUSER_PASSWORD = env('DJANGO_SUPERUSER_PASSWORD', default='admin')

FIXSTURES_DIR = BASE_DIR / 'core' / 'fixtures'
JSON_PARSER_FILE = 'data.json'
FIXSTURES_FILE = FIXSTURES_DIR / JSON_PARSER_FILE
RESOURSES_ROOT = BASE_DIR / 'resourses'

# Важен порядок ключей для вставки/удаления
FILE_MODEL_MAP = {
    'main_player_team': 'Player',
    'main_player': 'Player',
    'main_team': 'Team',
    'main_staffteammember': 'StaffTeamMember',
    'main_staffmember': 'StaffMember',
    'main_city': 'City',
    'main_nosology': 'Nosology',
    'main_discipline': 'Discipline',
    'main_disciplinename': 'DisciplineName',
    'main_disciplinelevel': 'DisciplineLevel',
}
