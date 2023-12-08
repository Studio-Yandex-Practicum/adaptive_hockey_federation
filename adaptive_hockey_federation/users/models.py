from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL, CharField, ForeignKey
from main.models import Team

NAME_MAX_LENGTH = 256
EMAIL_MAX_LENGTH = 256
PHONE_MAX_LENGTH = 20

ROLE_USER = 'user'
ROLE_AGENT = 'agent'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLES_CHOICES = (
    (ROLE_USER, 'Пользователь'),
    (ROLE_AGENT, 'Представитель команды'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)


class User(AbstractUser):
    phone = CharField(
        max_length=PHONE_MAX_LENGTH,
    )
    role = CharField(
        choices=ROLES_CHOICES,
        default=ROLE_USER,
        max_length=max(len(role) for role, _ in ROLES_CHOICES)
    )
    first_name = CharField(
        max_length=NAME_MAX_LENGTH,
        default='',
    )
    last_name = CharField(
        max_length=NAME_MAX_LENGTH,
        default='',
    )
    team = ForeignKey(
        to=Team,
        on_delete=SET_NULL,
        related_name='users',
        verbose_name='Команда',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_agent(self):
        return self.role == ROLE_AGENT

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    @property
    def is_admin(self):
        return (self.role == ROLE_ADMIN) or self.is_staff
