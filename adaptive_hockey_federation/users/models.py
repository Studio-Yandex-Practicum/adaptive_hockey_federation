from core.constants import (
    EMAIL_MAX_LENGTH,
    NAME_MAX_LENGTH,
    QUERY_SET_LENGTH,
    ROLE_ADMIN,
    ROLE_AGENT,
    ROLE_MODERATOR,
    ROLES_CHOICES,
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, поле 'username' исключено,
    идентификатором является поле с адресом электронной почты.
    """

    first_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name=_('Имя'),
        help_text=_('Имя'),
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name=_('Фамилия'),
        help_text=_('Фамилия'),
    )
    patronymic = models.CharField(
        blank=True,
        max_length=NAME_MAX_LENGTH,
        verbose_name=_('Отчество'),
        help_text=_('Отчество'),

    )
    role = models.CharField(
        choices=ROLES_CHOICES,
        default=ROLE_AGENT,
        max_length=max(len(role) for role, _ in ROLES_CHOICES),
        verbose_name=_('Роль'),
        help_text=_('Уровень прав доступа'),
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name=_('Электронная почта'),
        help_text=_('Электронная почта'),
    )
    phone = PhoneNumberField(
        blank=True,
        validators=[validate_international_phonenumber],
        verbose_name=_('Актуальный номер телефона'),
        help_text=_('Номер телефона, допустимый формат - +7 ХХХ ХХХ ХХ ХХ'),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Дата регистрации.'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Статус администратора.'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Показывает статус он-лайн.'),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('last_name',)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.email[:QUERY_SET_LENGTH].capitalize()

    def get_username(self):
        return (
            f'{self.first_name[:QUERY_SET_LENGTH]} '
            f'{self.last_name[:QUERY_SET_LENGTH]}'
        )

    def get_full_name(self):
        return (
            f'{self.first_name[:QUERY_SET_LENGTH]} '
            f'{self.patronymic[:QUERY_SET_LENGTH]} '
            f'{self.last_name[:QUERY_SET_LENGTH]}'
        )

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_agent(self):
        """
        Представитель команды - имеет возможность редактировать данные детей в
        своей команде. Просматривать некоторые данные по игрокам в других
        командах (ФИО, возраст, спортивный класс, тип заболевания).
        Выгружать формы по своей команде. Загружать сканы справок.
        """
        return self.role == ROLE_AGENT

    @property
    def is_moderator(self):
        """
        Модератор - имеет возможности вносить данные по определенному ребенку,
        не может добавлять новых пользователей и удалять детей, команды.
        """
        return self.role == ROLE_MODERATOR

    @property
    def is_admin(self):
        """
        Администратор - имеет неограниченные права управления на проекте.
        """
        return (self.role == ROLE_ADMIN) or self.is_staff
