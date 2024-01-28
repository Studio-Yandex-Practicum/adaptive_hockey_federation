from django.apps import AppConfig
from django.db.models.signals import post_migrate
from users.utils import set_default_permission_group


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'

    def ready(self):
        post_migrate.connect(set_default_permission_group, sender=self)
