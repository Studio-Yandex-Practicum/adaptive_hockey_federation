from core.constants import (
    CHAR_FIELD_LENGTH,
    CLASS_FIELD_LENGTH,
    DEFAULT_VALUE,
    EMPTY_VALUE_DISPLAY,
    GENDER_CHOICES,
    PLAYER_POSITION_CHOICES,
    STAFF_POSITION_CHOICES,
)
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.models import User


class BaseUniqueName(models.Model):
    name = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_("Наименование"),
        help_text=_("Наименование"),
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        abstract = True

    def __str__(self):
        return self.name


class City(BaseUniqueName):
    """
    Модель Город.
    """

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name

    @classmethod
    def get_by_name(cls, name: str):
        """Возвращает объект БД по наименованию (полю "name")."""
        name = name.strip()
        res: QuerySet = cls.objects.filter(name=name)
        if res.exists():
            return res.first()
        return None


class DisciplineName(BaseUniqueName):
    """
    Модель название дисциплин
    (следж-хоккей, хоккей для незрячих, спец. хоккей).
    """

    class Meta:
        verbose_name = "Название дисциплины"
        verbose_name_plural = "Названия дисциплин"

    def __str__(self):
        return self.name


class DisciplineLevel(BaseUniqueName):
    """
    Модель классификация, статусы дисциплин.
    """

    class Meta:
        verbose_name = "Классификация/статус дисциплины"
        verbose_name_plural = "Классификация/статусы дисциплин"

    def __str__(self):
        return self.name


class Discipline(models.Model):
    """
    Модель Дисциплина.
    """

    discipline_name = models.ForeignKey(
        DisciplineName,
        on_delete=models.CASCADE,
        max_length=CLASS_FIELD_LENGTH,
        verbose_name=_("Название дисциплины"),
        help_text=_("Название дисциплины"),
        related_name="disciplines",
    )
    discipline_level = models.ForeignKey(
        DisciplineLevel,
        on_delete=models.CASCADE,
        max_length=CLASS_FIELD_LENGTH,
        verbose_name=_("Класс/статус"),
        help_text=_("Класс/статус"),
        related_name="disciplines",
    )

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"
        constraints = [
            models.UniqueConstraint(
                name="discipline_name_level_unique",
                fields=["discipline_name", "discipline_level"],
            )
        ]

    def __str__(self):
        return f"{self.discipline_name.name} ({self.discipline_level.name})"


class Nosology(BaseUniqueName):
    """
    Модель Нозология.
    """

    class Meta:
        verbose_name = "Нозология"
        verbose_name_plural = "Нозология"

    def __str__(self):
        return self.name


class Diagnosis(BaseUniqueName):
    """
    Модель Диагноз.
    """

    nosology = models.ForeignKey(
        Nosology,
        on_delete=models.CASCADE,
        max_length=CLASS_FIELD_LENGTH,
        verbose_name=_("Нозология"),
        help_text=_("Нозология"),
        related_name="diagnosis",
    )

    class Meta:
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

    def __str__(self):
        return self.name


class BasePerson(models.Model):
    """
    Абстрактная модель с базовой персональной информацией.
    """

    surname = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_("Фамилия"),
        help_text=_("Фамилия"),
        default=EMPTY_VALUE_DISPLAY,
    )
    name = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_("Имя"),
        help_text=_("Имя"),
        default=EMPTY_VALUE_DISPLAY,
    )
    patronymic = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        blank=True,
        verbose_name=_("Отчество"),
        help_text=_("Отчество"),
        default=EMPTY_VALUE_DISPLAY,
    )

    class Meta:
        ordering = ("surname", "name", "patronymic")
        abstract = True

    def __str__(self):
        return " ".join([self.surname, self.name, self.patronymic])


class StaffMember(BasePerson):
    """
    Модель сотрудник.
    """

    phone = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        blank=True,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_("Номер телефона"),
        help_text=_("Номер телефона"),
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
        return " ".join([self.surname, self.name, self.patronymic])


class Team(BaseUniqueName):
    """
    Модель команды.
    """

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
        related_name='team'
    )

    class Meta:
        default_related_name = "teams"
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        constraints = [
            models.UniqueConstraint(
                name="team_city_unique",
                fields=["name", "city", "discipline_name"],
            )
        ]

    def __str__(self):
        if self.city:
            return f"{self.name} - {self.city}"
        return self.name


class StaffTeamMember(models.Model):
    """
    Модель сотрудник команды.
    """

    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        verbose_name=_("Сотрудник"),
        help_text=_("Сотрудник"),
    )
    staff_position = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        choices=STAFF_POSITION_CHOICES,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_("Статус сотрудника"),
        help_text=_("Статус сотрудника"),
    )
    team = models.ManyToManyField(
        Team,
        related_name="team_members",
        verbose_name=_("Команда"),
        help_text=_("Команда"),
    )
    qualification = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        default=EMPTY_VALUE_DISPLAY,
        blank=True,
        verbose_name=_("Квалификация"),
        help_text=_("Квалификация"),
    )
    notes = models.TextField(
        default=EMPTY_VALUE_DISPLAY,
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

    def __str__(self):
        return " ".join(
            [
                self.staff_member.surname,
                self.staff_member.name,
                self.staff_member.patronymic,
            ]
        )

    def get_name_and_staff_position(self):
        return f"{self.__str__()} ({self.staff_position})"


class Player(BasePerson):
    """
    Модель игрока. Связь с командой "многие ко многим" на случай включения
    игрока в сборную, помимо основного состава.
    """

    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.SET_NULL,
        null=True,
        related_name="player_diagnosis",
        verbose_name=_("Диагноз"),
        help_text=_("Диагноз"),
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        related_name="player_disciplines",
        verbose_name=_("Дисциплина"),
        help_text=_("Дисциплина"),
    )
    team = models.ManyToManyField(
        Team,
        related_name="team_players",
        verbose_name=_("Команда"),
        help_text=_("Команда"),
    )
    birthday = models.DateField(
        verbose_name=_("Дата рождения"), help_text=_("Дата рождения")
    )
    addition_date = models.DateField(
        verbose_name=_("Дата добавления"),
        default=timezone.now,
        help_text=_("Дата добавления в базу данных"),
    )
    gender = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        choices=GENDER_CHOICES,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_("Пол"),
        help_text=_("Пол"),
    )
    level_revision = models.TextField(
        verbose_name=_("Уровень ревизии"),
        help_text=_("Уровень ревизии"),
        default=EMPTY_VALUE_DISPLAY,
        blank=True,
    )
    position = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        choices=PLAYER_POSITION_CHOICES,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_("Игровая позиция"),
        help_text=_("Игровая позиция"),
    )
    number = models.IntegerField(
        default=DEFAULT_VALUE,
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
        default=EMPTY_VALUE_DISPLAY,
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

    def __str__(self):
        return " ".join([self.surname, self.name, self.patronymic])

    def get_name_and_position(self):
        return f"{self.__str__()} ({self.position})"


class Document(BaseUniqueName):
    """
    Модель Документы для загрузки.
    """

    name = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_("Наименование"),
        help_text=_("Наименование"),
    )
    file = models.FileField(
        upload_to="documents",
        max_length=CHAR_FIELD_LENGTH,
        unique=True,
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="player_documemts",
        verbose_name=_("Игрок"),
        help_text=_("Игрок"),
        default=EMPTY_VALUE_DISPLAY,
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
            )
        ]

    def __str__(self):
        return f"Документ игрока: {self.player}"
