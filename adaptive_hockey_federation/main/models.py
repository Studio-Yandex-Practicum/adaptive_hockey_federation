from django.db import models
from django.utils.translation import gettext_lazy as _

CHAR_FIELD_LENGTH = 256
EMPTY_VALUE_DISPLAY = ''
CLASS_FIELD_LENGTH = 10
DEFAULT_VALUE = 0

GENDER_CHOICES = (
    ('male', 'Мужской'),
    ('female', 'Женский'),
)

PLAYER_POSITION_CHOICES = (
    ('striker', 'Нападающий'),
    ('bobber', 'Поплавок'),
    ('goalkeeper', 'Вратарь'),
    ('defender', 'Защитник'),
)

STAFF_POSITION_CHOICES = (
    ('trainer', 'тренер'),
    ('other', 'другой'),
)


class BaseUniqueName(models.Model):
    name = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_('Наименование'),
        help_text=_('Наименование'),
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class City(BaseUniqueName):
    """
    Модель Город.
    """
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class DisciplineName(BaseUniqueName):
    """
    Модель название дисциплин
    (следж-хоккей, хоккей для незрячих, спец. хоккей).
    """
    class Meta:
        verbose_name = 'Название дисциплины'
        verbose_name_plural = 'Названия дисциплин'

    def __str__(self):
        return self.name


class DisciplineLevel(BaseUniqueName):
    """
    Модель классификация, статусы дисциплин.
    """
    class Meta:
        verbose_name = 'Классификация/статус дисциплины'
        verbose_name_plural = 'Классификация/статусы дисциплин'

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
        verbose_name=_('Название дисциплины'),
        help_text=_('Название дисциплины'),
        related_name='disciplines'
    )
    discipline_level = models.ForeignKey(
        DisciplineLevel,
        on_delete=models.CASCADE,
        max_length=CLASS_FIELD_LENGTH,
        verbose_name=_('Класс/статус'),
        help_text=_('Класс/статус'),
        related_name='disciplines'
    )

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        constraints = [
            models.UniqueConstraint(
                name='discipline_name_level_unique',
                fields=['discipline_name', 'discipline_level'],
            )
        ]

    def __str__(self):
        return self.discipline_name.name


class Nosology(BaseUniqueName):
    """
    Модель Нозология.
    """
    class Meta:
        verbose_name = 'Нозология'
        verbose_name_plural = 'Нозология'

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
        verbose_name=_('Нозология'),
        help_text=_('Нозология'),
        related_name='diagnosis'
    )

    class Meta:
        verbose_name = 'Диагноз'
        verbose_name_plural = 'Диагнозы'

    def __str__(self):
        return self.name


class Document(BaseUniqueName):
    """
    Модель Документы для загрузки.
    """
    file = models.FileField(
        upload_to='documents',
        max_length=CHAR_FIELD_LENGTH
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.name


class BasePerson(models.Model):
    """
    Абстрактная модель с базовой персональной информацией.
    """
    surname = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_('Фамилия'),
        help_text=_('Фамилия'),
        default=EMPTY_VALUE_DISPLAY
    )
    name = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name=_('Имя'),
        help_text=_('Имя'),
        default=EMPTY_VALUE_DISPLAY
    )
    patronymic = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        blank=True,
        verbose_name=_('Отчество'),
        help_text=_('Отчество'),
        default=EMPTY_VALUE_DISPLAY
    )

    class Meta:
        ordering = ('surname', 'name', 'patronymic')
        abstract = True

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])


class StaffMember(BasePerson):
    """
    Модель сотрудник.
    """
    phone = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        blank=True,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Номер телефона'),
        help_text=_('Номер телефона')
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])


class StaffTeamMember(models.Model):
    """
    Модель сотрудник команды.
    """
    staff_member = models.ForeignKey(
        StaffMember,
        on_delete=models.SET_DEFAULT,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Сотрудник'),
        help_text=_('Сотрудник')
    )
    staff_position = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        choices=STAFF_POSITION_CHOICES,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Статус сотрудника'),
        help_text=_('Статус сотрудника')
    )
    qualification = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        default=EMPTY_VALUE_DISPLAY,
        blank=True,
        verbose_name=_('Квалификация'),
        help_text=_('Квалификация')
    )
    notes = models.TextField(
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Описание'),
        help_text=_('Описание'),
        blank=True
    )

    class Meta:
        verbose_name = 'Сотрудник команды'
        verbose_name_plural = 'Сотрудники команды'

    def __str__(self):
        return ' '.join([
            self.staff_member.surname,
            self.staff_member.name,
            self.staff_member.patronymic
        ])


class Team(BaseUniqueName):
    """
    Модель команды.
    """
    city = models.ForeignKey(
        City,
        on_delete=models.SET_DEFAULT,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Город откуда команда'),
        help_text=_('Город откуда команда')
    )
    staff_team_member = models.ForeignKey(
        StaffTeamMember,
        on_delete=models.SET_DEFAULT,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Сотрудник команды'),
        help_text=_('Сотрудник команды')
    )
    discipline_name = models.ForeignKey(
        DisciplineName,
        on_delete=models.SET_DEFAULT,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Дисциплина команды'),
        help_text=_('Дисциплина команды')
    )
    # models User
    # curator = None

    class Meta:
        default_related_name = 'teams'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        constraints = [
            models.UniqueConstraint(
                name='team_city_unique',
                fields=['name', 'city', 'discipline_name'],
            )
        ]

    def __str__(self):
        if self.city:
            return f'{self.name} - {self.city}'
        return self.name


class Player(BasePerson):
    """
    Модель игрока. Связь с командой "многие ко многим" на случай включения
    игрока в сборную, помимо основного состава.
    """
    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.SET_NULL,
        null=True,
        related_name='player_diagnosis',
        verbose_name=_('Диагноз'),
        help_text=_('Диагноз'),
        default=DEFAULT_VALUE
    )
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        null=True,
        related_name='player_disciplines',
        verbose_name=_('Дисциплина'),
        help_text=_('Дисциплина'),
        default=EMPTY_VALUE_DISPLAY
    )
    team = models.ManyToManyField(
        Team,
        related_name='team_players',
        verbose_name=_('Команда'),
        help_text=_('Команда')
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='player_documemts',
        verbose_name=_('Документ'),
        help_text=_('Документ'),
        default=EMPTY_VALUE_DISPLAY,
        blank=True,
        null=True
    )
    birthday = models.DateField(
        verbose_name=_('Дата рождения'),
        help_text=_('Дата рождения')
    )
    gender = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        choices=GENDER_CHOICES,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Пол'),
        help_text=_('Пол')
    )
    level_revision = models.TextField(
        verbose_name=_('Уровень ревизии'),
        help_text=_('Уровень ревизии'),
        default=EMPTY_VALUE_DISPLAY,
        blank=True
    )
    position = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        choices=PLAYER_POSITION_CHOICES,
        default=EMPTY_VALUE_DISPLAY,
        verbose_name=_('Игровая позиция'),
        help_text=_('Игровая позиция')
    )
    number = models.IntegerField(
        default=DEFAULT_VALUE,
        verbose_name=_('Номер игрока'),
        help_text=_('Номер игрока')
    )
    is_captain = models.BooleanField(
        default=False,
        verbose_name=_('Капитан'),
        help_text=_('Капитан')
    )
    is_assistent = models.BooleanField(
        default=False,
        verbose_name=_('Ассистент'),
        help_text=_('Ассистент')
    )
    identity_document = models.TextField(
        verbose_name=_('Удостоверение личности'),
        help_text=_('Удостоверение личности'),
        default=EMPTY_VALUE_DISPLAY,
        blank=True
    )

    class Meta(BasePerson.Meta):
        default_related_name = 'players'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        constraints = [
            models.UniqueConstraint(
                name='player_unique',
                fields=[
                    'name',
                    'surname',
                    'patronymic',
                    'birthday',
                ]
            ),
            models.UniqueConstraint(
                name='player_position_number_unique',
                fields=[
                    'position',
                    'number'
                ]
            )
        ]

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])
