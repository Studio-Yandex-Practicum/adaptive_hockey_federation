from datetime import date

from django.db.models import (
    BooleanField, CASCADE, CharField, CheckConstraint, DateField, F,
    ForeignKey, ManyToManyField, Model, Q, SET_NULL, UniqueConstraint,
)

SEX_CHOICES = (
    ('male', 'Мужской'),
    ('female', 'Женский'),
)

NAME_FIELD_LENGTH = 256
BASE_PERSONAL_FIELD_LENGTH = 256


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
    Город для указания родного города команды или места проведения соревнования
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


class Competition(Model):
    name = CharField(
        max_length=NAME_FIELD_LENGTH,
        unique_for_date='start_date',
    )
    start_date = DateField(
        verbose_name='Дата начала состязания',
    )
    end_date = DateField(
        verbose_name='Дата окончания состязания',
    )
    team = ManyToManyField(
        to=Team,
        related_name='competition_teams',
        through='CompetitionTeam',
    )
    location = ForeignKey(
        to=Location,
        related_name='competitions',
        on_delete=SET_NULL,
    )

    @property
    def is_active(self):
        return self.end_date >= date.today()

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
        constraints = [
            CheckConstraint(
                check=Q(end_date__gt=F('start_date')),
                name='dates_start_end_verification'
            ),
        ]


class CompetitionTeam(Model):
    team = ForeignKey(
        to=Team,
        related_name='competitions',
        on_delete=CASCADE
    )
    competition = ForeignKey(
        to=Competition,
        related_name='teams',
        on_delete=CASCADE
    )


class Position(BaseUniqueName):
    """
    Позиция игрока в команде
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'


class TrainerQualification(BaseUniqueName):
    """
    Квалификационные категории тренера (высшая, первая, вторая)
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Квалификационная категория'
        verbose_name_plural = 'Квалификационные категории'


class PlayerQualification(TrainerQualification):
    """
    Квалификационные категории игрока (спортивные разряды и прочее, наверное)
    """
    pass

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Разряд игрока'
        verbose_name_plural = 'Разряды игроков'


class Role(BaseUniqueName):
    """
    Роль игрока (капитан, ассистент)
    """
    pass


class Anamnes(BaseUniqueName):
    """
    Диагноз, числовой статус, коляска
    """
    wheelchair = BooleanField(
        default=False,
        verbose_name='На коляске'
    )


class BasePerson(Model):
    """
    Абстрактная модель с базовой персональной информацией
    """
    name = CharField(
        max_length=BASE_PERSONAL_FIELD_LENGTH,
        verbose_name='Имя',
    )
    surname = CharField(
        max_length=BASE_PERSONAL_FIELD_LENGTH,
        verbose_name='Фамилия',
    )
    patronymic = CharField(
        max_length=BASE_PERSONAL_FIELD_LENGTH,
        blank=True,
        verbose_name='Отчество',
    )

    class Meta:
        ordering = ('surname', 'name', 'patronymic')
        abstract = True

    def __str__(self):
        return ' '.join([self.surname, self.name, self.patronymic])


class Player(BasePerson):
    birth_date = DateField()
    sex = CharField(
        max_length=max(len(sex) for sex, _ in SEX_CHOICES),
        choices=SEX_CHOICES,
        blank=True,
        null=True,
        verbose_name='Пол'
    )
    anamnes = ForeignKey(
        to=Anamnes,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Дигноз или числовой статус',
    )
    qualification = ForeignKey(
        to=PlayerQualification,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Разряд игрока'
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


class PlayerTeam(Model):
    player = ForeignKey(
        to=Player,
        related_name='teams',
        on_delete=CASCADE,
        verbose_name='Игрок',

    )
    team = ForeignKey(
        to=Team,
        related_name='players',
        on_delete=CASCADE,
        verbose_name='Команда',
    )
    position = ForeignKey(
        to=Position,
        on_delete=SET_NULL,
        verbose_name='Позиция игрока'
    )
