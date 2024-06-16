from typing import TYPE_CHECKING

from core.constants import (GENDER_CHOICES, PLAYER_POSITION_CHOICES,
                            STAFF_POSITION_CHOICES, MainConstantsInt,
                            MainConstantsStr)
from core.validators import fio_validator, validate_date_birth
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from users.models import User
from users.validators import zone_code_without_seven_hundred

if TYPE_CHECKING:
    from django.db.models import QuerySet


class BaseUniqueName(models.Model):
    """Базовый класс для других моделей с повторяющимся полем name."""

    name = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        verbose_name=_("Наименование"),
        help_text=_("Наименование"),
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        abstract = True

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name

    @classmethod
    def get_by_name(cls, name: str):
        """Возвращает объект БД по наименованию (полю "name")."""
        name = name.strip()
        res: QuerySet = cls.objects.filter(name=name)  # type: ignore
        if res.exists():
            return res.first()
        return None


class City(BaseUniqueName):
    """Модель Город."""

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class DisciplineName(BaseUniqueName):
    """Модель дисциплин (следж-хоккей, хоккей для незрячих, спец. хоккей)."""

    class Meta:
        verbose_name = "Название дисциплины"
        verbose_name_plural = "Названия дисциплин"

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class DisciplineLevel(BaseUniqueName):
    """Модель классификация, статусы дисциплин."""

    name = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        verbose_name=_("Наименование"),
        help_text=_("Наименование"),
    )

    discipline_name = models.ForeignKey(
        DisciplineName,
        on_delete=models.CASCADE,
        verbose_name=_("Дисциплина"),
        help_text=_("Дисциплина"),
        related_name="levels",
    )

    class Meta:
        verbose_name = "Классификация/статус дисциплины"
        verbose_name_plural = "Классификация/статусы дисциплин"

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class Nosology(BaseUniqueName):
    """Модель Нозология."""

    class Meta:
        verbose_name = "Нозология"
        verbose_name_plural = "Нозология"

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class Diagnosis(BaseUniqueName):
    """Модель Диагноз."""

    nosology = models.ForeignKey(
        Nosology,
        on_delete=models.CASCADE,
        max_length=MainConstantsInt.CLASS_FIELD_LENGTH,
        verbose_name=_("Нозология"),
        help_text=_("Нозология"),
        related_name="diagnosis",
    )

    class Meta:
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

    def __str__(self):
        """Метод, использующий поле name для строкового представления."""
        return self.name


class BasePerson(models.Model):
    """Абстрактная модель с базовой персональной информацией."""

    surname = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        verbose_name=_("Фамилия"),
        help_text=_("Фамилия"),
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        validators=[fio_validator()],
    )
    name = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        verbose_name=_("Имя"),
        help_text=_("Имя"),
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        validators=[fio_validator()],
    )
    patronymic = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        blank=True,
        verbose_name=_("Отчество"),
        help_text=_("Отчество"),
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        validators=[fio_validator()],
    )

    class Meta:
        ordering = ("surname", "name", "patronymic")
        abstract = True

    def __str__(self):
        """Метод, использующий полное ФИО для строкового представления."""
        return " ".join([self.surname, self.name, self.patronymic])


class StaffMember(BasePerson):
    """Модель сотрудник."""

    phone = PhoneNumberField(
        blank=True,
        validators=[
            validate_international_phonenumber,
            zone_code_without_seven_hundred,
        ],
        verbose_name=_("Актуальный номер телефона"),
        help_text=_("Номер телефона, допустимый формат - +7 ХХХ ХХХ ХХ ХХ"),
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        constraints = [
            models.UniqueConstraint(
                name="staff_member_unique",
                fields=[
                    "name",
                    "surname",
                    "patronymic",
                ],
            ),
        ]

    def __str__(self):
        """Метод, использующий полное ФИО для строкового представления."""
        return " ".join([self.surname, self.name, self.patronymic])


class Team(BaseUniqueName):
    """Модель команды."""

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name=_("Город откуда команда"),
        help_text=_("Город откуда команда"),
    )
    discipline_name = models.ForeignKey(
        DisciplineName,
        on_delete=models.CASCADE,
        verbose_name=_("Дисциплина команды"),
        help_text=_("Дисциплина команды"),
    )
    curator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Куратор команды"),
        help_text=_("Куратор команды"),
        related_name="team",
    )

    class Meta:
        default_related_name = "teams"
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        constraints = [
            models.UniqueConstraint(
                name="team_city_unique",
                fields=["name", "city", "discipline_name"],
            ),
        ]
        permissions = [
            ("list_view_team", "Can view list of Команда"),
        ]

    def __str__(self):
        """Метод, определяющий строковое представление объекта."""
        if self.city:
            return f"{self.name} - {self.city}"
        return self.name


class StaffTeamMember(models.Model):
    """Модель сотрудник команды."""

    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        verbose_name=_("Сотрудник"),
        help_text=_("Сотрудник"),
    )
    staff_position = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        choices=STAFF_POSITION_CHOICES,
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        verbose_name=_("Статус сотрудника"),
        help_text=_("Статус сотрудника"),
    )
    team = models.ManyToManyField(
        Team,
        related_name="team_members",
        verbose_name=_("Команда"),
        help_text=_("Команда"),
        default="Свободный агент",
        blank=True,
    )
    qualification = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        blank=True,
        verbose_name=_("Квалификация"),
        help_text=_("Квалификация"),
    )
    notes = models.TextField(
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        verbose_name=_("Описание"),
        help_text=_("Описание"),
        blank=True,
    )

    class Meta:
        verbose_name = "Сотрудник команды"
        verbose_name_plural = "Сотрудники команды"
        constraints = [
            models.UniqueConstraint(
                name="staff_member_position_unique",
                fields=[
                    "staff_member",
                    "staff_position",
                ],
            ),
        ]
        permissions = [
            ("list_view_staff", "Can view list of Персонала команды"),
        ]

    def __str__(self):
        """Метод, использующий полное ФИО для строкового представления."""
        return " ".join(
            [
                self.staff_member.surname,
                self.staff_member.name,
                self.staff_member.patronymic,
            ],
        )

    def get_name_and_staff_position(self):
        """Метод для получения строки с данными сотрудника команды."""
        return f"{self.__str__()} ({self.staff_position})"


class Player(BasePerson):
    """
    Модель игрока.

    Связь с командой "многие ко многим" на случай включения игрока
    в сборную, помимо основного состава.
    """

    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.SET_NULL,
        null=True,
        related_name="player_diagnosis",
        verbose_name=_("Диагноз"),
        help_text=_("Диагноз"),
    )
    discipline_name = models.ForeignKey(
        DisciplineName,
        on_delete=models.SET_NULL,
        null=True,
        related_name="player_disciplines_names",
        verbose_name=_("Дисциплина"),
        help_text=_("Дисциплина"),
    )
    discipline_level = models.ForeignKey(
        DisciplineLevel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="player_disciplines_levels",
        verbose_name=_("Числовой статус"),
        help_text=_("Числовой статус"),
    )
    team = models.ManyToManyField(
        Team,
        related_name="team_players",
        verbose_name=_("Команда"),
        help_text=_("Команда"),
    )
    birthday = models.DateField(
        verbose_name=_("Дата рождения"),
        help_text=_("Дата рождения"),
        validators=[validate_date_birth],
    )
    addition_date = models.DateField(
        verbose_name=_("Дата добавления"),
        default=timezone.now,
        help_text=_("Дата добавления в базу данных"),
    )
    gender = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        choices=GENDER_CHOICES,
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        verbose_name=_("Пол"),
        help_text=_("Пол"),
    )
    level_revision = models.TextField(
        verbose_name=_("Игровая классификация"),
        help_text=_("Игровая классификация"),
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        blank=True,
    )
    position = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        choices=PLAYER_POSITION_CHOICES,
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        verbose_name=_("Игровая позиция"),
        help_text=_("Игровая позиция"),
    )
    number = models.IntegerField(
        default=MainConstantsInt.DEFAULT_VALUE,
        verbose_name=_("Номер игрока"),
        help_text=_("Номер игрока"),
    )
    is_captain = models.BooleanField(
        default=False,
        verbose_name=_("Капитан"),
    )
    is_assistent = models.BooleanField(
        default=False,
        verbose_name=_("Ассистент"),
    )
    identity_document = models.TextField(
        verbose_name=_("Удостоверение личности"),
        help_text=_("Удостоверение личности"),
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        blank=True,
    )

    class Meta(BasePerson.Meta):
        default_related_name = "players"
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
        # TODO Раскомментировать, когда будет ручное добавление игроков
        # ограничение на дублирование записей
        constraints = [
            models.UniqueConstraint(
                name="player_unique",
                fields=[
                    "name",
                    "surname",
                    "patronymic",
                    "birthday",
                    # 'position',
                    # 'number'
                ],
            ),
        ]
        permissions = [
            ("list_view_player", "Can view list of Игрок"),
        ]

    def __str__(self):
        """Метод, использующий полное ФИО для строкового представления."""
        return " ".join([self.surname, self.name, self.patronymic])

    def get_name_and_position(self):
        """Метод для получения строки с данными игрока и его позицией."""
        return f"{self.__str__()} ({self.position})"


class Document(BaseUniqueName):
    """Модель Документы для загрузки."""

    name = models.CharField(
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        verbose_name=_("Наименование"),
        help_text=_("Наименование"),
    )
    file = models.FileField(
        upload_to="players_documents",
        max_length=MainConstantsInt.CHAR_FIELD_LENGTH,
        unique=True,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="player_documemts",
        verbose_name=_("Игрок"),
        help_text=_("Игрок"),
        default=MainConstantsStr.EMPTY_VALUE_DISPLAY,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        constraints = [
            models.UniqueConstraint(
                name="player_docume_unique",
                fields=["file", "player"],
            ),
        ]

    def __str__(self):
        """Метод, определяющий строковое представление объекта."""
        return f"Документ игрока: {self.player}"


@receiver(post_delete, sender=Document)
def document_file_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
