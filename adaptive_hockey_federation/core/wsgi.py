import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.config.dev_settings",
)

application = get_wsgi_application()
