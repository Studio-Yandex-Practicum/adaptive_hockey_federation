from django.db import models
from django.utils.translation import gettext_lazy as _

NAME_FIELD_LENGTH = 256
EMPTY_VALUE_DISPLAY = '--пусто--'
CLASS_FIELD_LENGTH = 10


class BaseUniqueName(models.Model):
    name = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Название'),
        help_text=_('Название'),
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class BasePerson(models.Model):
    """
    Абстрактная модель с базовой персональной информацией.
    """
    surname = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Фамилия'),
        help_text=_('Фамилия'),
        default=EMPTY_VALUE_DISPLAY
    )
    name = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Имя'),
        help_text=_('Имя'),
        default=EMPTY_VALUE_DISPLAY
    )
    patronymic = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        blank=True,
        verbose_name=_('Отчество'),
        help_text=_('Отчество'),
        default=EMPTY_VALUE_DISPLAY
    )
    date_of_birth = models.DateField(
        verbose_name=_('Дата рождения'),
        help_text=_('Дата рождения'),
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('surname', 'name', 'patronymic')
        abstract = True

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])


class Diagnosis(models.Model):
    """
    Модель Диагноз.
    """
    class_name = models.CharField(
        verbose_name=_('Класс'),
        help_text=_('Класс'),
        max_length=CLASS_FIELD_LENGTH,
        unique=True
    )
    is_wheeled = models.BooleanField(
        default=False,
        verbose_name=_('На коляске'),
        help_text=_('На коляске')
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        help_text=_('Описание'),
        blank=True
    )

    class Meta:
        verbose_name = 'Диагноз'
        verbose_name_plural = 'Диагнозы'

    def __str__(self):
        return self.class_name


class Gender(BaseUniqueName):
    """
    Модель Пол.
    """
    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.name


class Position(BaseUniqueName):
    """
    Модель Игоровая позиция.
    """
    class Meta:
        verbose_name = 'Игоровая позиция'
        verbose_name_plural = 'Игровые позиции'


class Qualification(BaseUniqueName):
    """
    Модель Квалификация.
    """
    class Meta:
        verbose_name = 'Квалификация'
        verbose_name_plural = 'Квалификации'


class Discipline(BaseUniqueName):
    """
    Модель Дисциплина.
    """
    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class City(BaseUniqueName):
    """
    Модель Город.
    """
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Player(BasePerson):
    """
    Модель игрока. Связь с командой "многие ко многим" на случай включения
    игрока в сборную, помимо основного состава.
    """
    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.CASCADE,
        related_name='diagnosis',
        verbose_name=_('Диагноз'),
        help_text=_('Диагноз'),
        default=0
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.CASCADE,
        related_name='gender',
        verbose_name=_('Пол'),
        help_text=_('Пол'),
        default=0
    )
    identification_card = models.TextField(
        verbose_name=_('Удостоверение личности'),
        help_text=_('Удостоверение личности'),
        default=0
    )

    class Meta(BasePerson.Meta):
        default_related_name = 'players'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        constraints = [
            models.UniqueConstraint(
                name='player_unique',
                fields=['name', 'surname', 'patronymic', 'date_of_birth']
            )
        ]


class Trainer(BasePerson):
    """
    Модель Тренер.
    """
    description = models.TextField(
        verbose_name=_('Описание'),
        help_text=_('Описание')
    )

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'


class Team(models.Model):
    """
    Модель команды.
    """
    name = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Название'),
        help_text=_('Название')
    )
    city = models.ForeignKey(
        to=City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Город откуда команда'),
        help_text=_('Город откуда команда')
    )
    discipline = models.ForeignKey(
        to=Discipline,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Дисциплина команды'),
        help_text=_('Дисциплина команды')
    )
    composition = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Состав'),
        help_text=_('Состав'),
        default=EMPTY_VALUE_DISPLAY
    )
    age = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Возраст'),
        help_text=_('Возраст'),
        default=EMPTY_VALUE_DISPLAY
    )

    class Meta:
        default_related_name = 'teams'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        constraints = [
            models.UniqueConstraint(
                name='team_city_unique',
                fields=['name', 'city', 'discipline'],
            )
        ]

    def __str__(self):
        if self.city:
            return f'{self.name} - {self.city}'
        return self.name


class TrainerTeam(models.Model):
    """
    Модель тренер - команда.
    """
    trainer = models.ForeignKey(
        to=Trainer,
        on_delete=models.CASCADE,
        verbose_name=_('Тренер команды'),
        help_text=_('Тренер команды')
    )
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        verbose_name=_('Команда'),
        help_text=_('Команда')
    )

    class Meta:
        default_related_name = 'trainer_teams'
        verbose_name = 'Тренер --> команда'
        verbose_name_plural = 'Тренер --> команды'
        constraints = [
            models.UniqueConstraint(
                name='trainer_teams_unique',
                fields=['trainer', 'team']
            )
        ]

    def __str__(self):
        return str(self.trainer.id)


class PlayerTeam(models.Model):
    """
    Связь "многие ко многим" игрока с командой с добавлением данных игрока
    в этой команде.
    """
    player = models.ForeignKey(
        to=Player,
        related_name='player_teams',
        on_delete=models.CASCADE,
        verbose_name=_('Игрок'),
        help_text=_('Игрок')

    )
    team = models.ForeignKey(
        to=Team,
        related_name='team_players',
        on_delete=models.CASCADE,
        verbose_name=_('Команда'),
        help_text=_('Команда')
    )
    position = models.ForeignKey(
        to=Position,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Позиция игрока'),
        help_text=_('Позиция игрока')
    )
    qualification = models.ForeignKey(
        to=Qualification,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Квалификация игрока'),
        help_text=_('Квалификация игрока')
    )
    number = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Номер игорока'),
        help_text=_('Номер игорока')
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

    class Meta:
        verbose_name = 'Игрок команды'
        verbose_name_plural = 'Игроки команды'

    def __str__(self):
        return str(self.player.id)


class Competition(BaseUniqueName):
    """
    Модель Соревнования.
    """
    city = models.ForeignKey(
        to=City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Город'),
        help_text=_('Город')
    )
    number = models.CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name=_('Номер соревнований'),
        help_text=_('Номер соревнований')
    )
    date = models.DateField(
        verbose_name=_('Дата соревнований'),
        help_text=_('Дата соревнований')
    )
    duration = models.IntegerField(
        default=0,
        verbose_name=_('Длительность'),
        help_text=_('Длительность')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активно'),
        help_text=_('Активно')
    )

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        constraints = [
            models.UniqueConstraint(
                name='competitions_unique',
                fields=['city', 'number', 'date']
            )
        ]

    def __str__(self):
        return str(self.city.id)


class TeamCompetition(models.Model):
    """
    Модель команда - соревнование.
    """
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        verbose_name=_('Команда'),
        help_text=_('Команда')
    )
    competition = models.ForeignKey(
        to=Competition,
        on_delete=models.CASCADE,
        verbose_name=_('Соревнование'),
        help_text=_('Соревнование')
    )

    class Meta:
        default_related_name = 'team_competitions'
        verbose_name = 'Соревнование --> команда'
        verbose_name_plural = 'Совревнования --> команды'
        constraints = [
            models.UniqueConstraint(
                name='competition_teams_unique',
                fields=['team', 'competition']
            )
        ]

    def __str__(self):
        return str(self.team.id)
