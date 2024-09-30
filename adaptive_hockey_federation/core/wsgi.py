import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    # при разработке core.config.dev_settings
    "DJANGO_SETTINGS_MODULE",
    "core.config.prod_settings",
)

application = get_wsgi_application()
