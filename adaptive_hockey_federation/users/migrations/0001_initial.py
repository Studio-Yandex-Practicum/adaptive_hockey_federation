# Generated by Django 4.2.11 on 2024-03-10 00:54

import django.contrib.auth.models
import django.core.validators
import django.utils.timezone
import phonenumber_field.modelfields
import phonenumber_field.validators as phone_field
import users.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProxyGroup",
            fields=[],
            options={
                "verbose_name": "Группа",
                "verbose_name_plural": "Группы",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.group",),
            managers=[
                ("objects", django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(
                    max_length=128,
                    verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all"
                        "permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Имя",
                        max_length=256,
                        verbose_name="Имя"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        help_text="Фамилия",
                        max_length=256,
                        verbose_name="Фамилия"
                    ),
                ),
                (
                    "patronymic",
                    models.CharField(
                        blank=True,
                        help_text="Отчество",
                        max_length=256,
                        verbose_name="Отчество",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Представитель команды", "Представитель команды"),
                            ("Модератор", "Модератор"),
                            ("Администратор", "Администратор"),
                            ("admin", "Суперпользователь"),
                        ],
                        default="Представитель команды",
                        help_text="Уровень прав доступа",
                        max_length=21,
                        verbose_name="Роль",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Электронная почта",
                        max_length=256,
                        unique=True,
                        validators=[
                            django.core.validators.EmailValidator(
                                message="Используйте корректный адрес"
                                "электронной почты. Адрес должен быть"
                                "не длиннее 150 символов. Допускается"
                                "использование латинских букв, цифр"
                                "и символов @/./+/-/_"
                            )
                        ],
                        verbose_name="Электронная почта",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="Номер телефона, допустимый формат"
                        "- +7 ХХХ ХХХ ХХ ХХ",
                        max_length=128,
                        region=None,
                        validators=[
                            phone_field.validate_international_phonenumber
                        ],
                        verbose_name="Актуальный номер телефона",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата регистрации.",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False, verbose_name="Статус администратора."
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, verbose_name="Показывает статус он-лайн."
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to."
                        "A user will get all permissions granted to"
                        "each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ("last_name",),
                "permissions": [
                    ("list_view_user", "Может видеть список пользователей")
                ],
            },
            managers=[
                ("objects", users.managers.CustomUserManager()),
            ],
        ),
    ]
