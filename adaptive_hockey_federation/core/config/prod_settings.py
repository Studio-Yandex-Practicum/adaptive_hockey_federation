from .base_settings import *

ROOT_DIR = BASE_DIR.parent

env.read_env(ROOT_DIR / ".env")

DEBUG = False

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE"),
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
# TODO: возможно удаления т.к относится к parser
FIXSTURES_DIR = BASE_DIR / "core" / "fixtures"
# TODO: возможно удаления т.к относится к parser
JSON_PARSER_FILE = "data.json"
# TODO: возможно удаления т.к относится к parser
FIXSTURES_FILE = FIXSTURES_DIR / JSON_PARSER_FILE
RESOURSES_ROOT = BASE_DIR / "resourses"

# Важен порядок ключей для вставки/удаления
FILE_MODEL_MAP = {
    "main_player_team": "Player",
    "main_player": "Player",
    "main_team": "Team",
    "main_staffteammember": "StaffTeamMember",
    "main_staffmember": "StaffMember",
    "main_city": "City",
    "main_diagnosis": "Diagnosis",
    "main_nosology": "Nosology",
    "main_disciplinelevel": "DisciplineLevel",
    "main_disciplinename": "DisciplineName",
}

EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

EMAIL_TEMPLATE_NAME = "emailing/email.html"

EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.yandex.ru")

try:
    EMAIL_PORT = env.int("EMAIL_PORT", default=587)
except ValueError:
    EMAIL_PORT = 587

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="example@yandex.ru")

EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="password")

EMAIL_USE_TLS = env.str("EMAIL_USE_TLS", default=True)

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SERVER_EMAIL = EMAIL_HOST_USER

EMAIL_ADMIN = EMAIL_HOST_USER

ADMIN_PAGE_ORDERING = {
    "main": [
        "Player",
        "Team",
        "StaffMember",
        "DisciplineName",
        "DisciplineLevel",
        "City",
        "Nosology",
        "Diagnosis",
        "GameDataPlayer",
    ],
}
