from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    ForeignKey,
    ManyToManyField,
    Model,
    UniqueConstraint,
)

SEX_CHOICES = (
    ('male', 'Мужской'),
    ('female', 'Женский'),
)

NAME_FIELD_LENGTH = 256
BASE_PERSON_FIELD_LENGTH = 256


class BaseUniqueName(Model):
    """
    Абстрактный класс с уникальным полем "Название" и методом отображения
    """
    name = CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name='Название',
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class Location(BaseUniqueName):
    """
    Локация привязки команды (город, область, край)
    или места проведения соревнования
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Территория'
        verbose_name_plural = 'Территории'


class Discipline(BaseUniqueName):
    """
    Классификация дисциплины (следж-хоккей, хоккей для незрячих, спец. хоккей)
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class Team(Model):
    """
    Модель команды.
    """
    name = CharField(max_length=NAME_FIELD_LENGTH, )
    location = ForeignKey(
        to=Location,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Локация команды',
    )
    discipline = ForeignKey(
        to=Discipline,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Дисциплина команды',
    )

    class Meta:
        default_related_name = 'teams'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        constraints = [
            UniqueConstraint(
                name='team_location_unique',
                fields=['name', 'location', 'discipline'],
            )
        ]

    def __str__(self):
        if self.location:
            return f'{self.name} - {self.location}'
        return self.name


class Position(BaseUniqueName):
    """
    Игровая позиция игрока в команде
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Игровая позиция'
        verbose_name_plural = 'Игровые позиции'


class Role(BaseUniqueName):
    """
    Роль игрока в команде (капитан, ассистент)
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Игровая позиция'
        verbose_name_plural = 'Игровые позиции'


class Anamnesis(BaseUniqueName):
    """
    Диагноз общий
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Диагноз'
        verbose_name_plural = 'Диагнозы'


class RespiratoryFailure(BaseUniqueName):
    """
    Класс хронической дыхательной недостаточности
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Класс ХДН'
        verbose_name_plural = 'Классы ХДН'


class BasePerson(Model):
    """
    Абстрактная модель с базовой персональной информацией
    """
    name = CharField(
        max_length=BASE_PERSON_FIELD_LENGTH,
        verbose_name='Имя',
    )
    surname = CharField(
        max_length=BASE_PERSON_FIELD_LENGTH,
        verbose_name='Фамилия',
    )
    patronymic = CharField(
        max_length=BASE_PERSON_FIELD_LENGTH,
        blank=True,
        default='',
        verbose_name='Отчество',
    )

    class Meta:
        ordering = ('surname', 'name', 'patronymic')
        abstract = True

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])


class Player(BasePerson):
    """
    Модель игрока. Связь с командой "многие ко многим" на случай включения
    игрока в сборную, помимо основного состава.
    """
    birth_date = DateField()
    sex = CharField(
        max_length=max(len(sex) for sex, _ in SEX_CHOICES),
        choices=SEX_CHOICES,
        blank=True,
        null=True,
        verbose_name='Пол'
    )
    team = ManyToManyField(
        to=Team,
        through='PlayerTeam',
        verbose_name='Команда'
    )

    class Meta(BasePerson.Meta):
        default_related_name = 'players'
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        constraints = [
            UniqueConstraint(
                name='player_unique',
                fields=['name', 'surname', 'patronymic', 'birth_date'],
            )
        ]


class Health(Model):
    """
    Информация по хронической дыхательной недостаточности.
    """
    player = ForeignKey(
        to=Player,
        related_name='health',
        on_delete=CASCADE,
        verbose_name='Игрок',
    )
    respiratory_failure = ForeignKey(
        to=RespiratoryFailure,
        related_name='respiratory_failure_players',
        on_delete=CASCADE,
        verbose_name='Класс ХДН',
    )
    is_permanent = BooleanField(
        default=False,
        verbose_name='Класс ХДН подтверждён перманентно',
    )
    revision = CharField(
        max_length=NAME_FIELD_LENGTH,
        blank=True,
        null=True,
        verbose_name='Пересмотр класса ХДН',
    )
    anamnesis = ForeignKey(
        to=Anamnesis,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Диагноз',
    )
    wheelchair = BooleanField(
        default=False,
        verbose_name='На коляске'
    )

    def __str__(self):
        return (f'Медицинские показатели'
                f' игрока {self.player.surname} {self.player.name}')


class PlayerTeam(Model):
    """
    Связь "многие ко многим" игрока с командой с добавлением данных игрока
    в этой команде.
    """
    player = ForeignKey(
        to=Player,
        related_name='player_teams',
        on_delete=CASCADE,
        verbose_name='Игрок',

    )
    team = ForeignKey(
        to=Team,
        related_name='team_players',
        on_delete=CASCADE,
        verbose_name='Команда',
    )
    position = ForeignKey(
        to=Position,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Позиция игрока',
    )
    role = ForeignKey(
        to=Role,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Статус игрока',
    )
    number = CharField(
        max_length=NAME_FIELD_LENGTH,
        verbose_name='Игровой номер',
    )
