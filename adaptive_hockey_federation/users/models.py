from django.contrib.auth.models import AbstractUser
from django.db import models  # noqa

ROLES_CHOICES = (
    (settings.ROLE_USER, 'Пользователь'),
    (settings.ROLE_MODERATOR, 'Модератор'),
    (settings.ROLE_ADMIN, 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(
            validate_non_reserved,
            validate_username_allowed_chars
        )
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH
    )
    role = models.CharField(
        choices=ROLES_CHOICES,
        default=settings.ROLE_USER,
        max_length=max(len(role) for role,_ in ROLES_CHOICES)
    )
    bio = models.TextField(blank=True, null=True)
    confirmation_code = models.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=settings.LAST_NAME_MAX_LENGTH,
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
    def is_moderator(self):
        return self.role == settings.ROLE_MODERATOR

    @property
    def is_admin(self):
        return (self.role == settings.ROLE_ADMIN) or self.is_staff
