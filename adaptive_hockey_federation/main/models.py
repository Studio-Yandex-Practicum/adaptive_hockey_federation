from datetime import date

from django.db.models import (
    BooleanField, CASCADE, CharField, CheckConstraint, DateField, F,
    ForeignKey, ManyToManyField, Model, OneToOneField, Q, SET_NULL,
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


class Competition(Model):
    """
    Модель для соревнований. Позже возможно будет добавлена связь с играми.
    """
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
        blank=True,
        null=True,
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


class PlayerPosition(BaseUniqueName):
    """
    Игровая позиция игрока в команде
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Игровая позиция'
        verbose_name_plural = 'Игровые позиции'


class CoachPosition(BaseUniqueName):
    """
    Название должности тренера в команде
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class CoachQualification(BaseUniqueName):
    """
    Квалификационные категории тренера (высшая, первая, вторая)
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Квалификационная категория'
        verbose_name_plural = 'Квалификационные категории'


class PlayerQualification(BaseUniqueName):
    """
    Квалификационные категории игрока (спортивные разряды и прочее, наверное)
    """

    class Meta(BaseUniqueName.Meta):
        verbose_name = 'Разряд игрока'
        verbose_name_plural = 'Разряды игроков'


class PlayerRole(BaseUniqueName):
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


class HealthCard(BaseUniqueName):
    """
    Медицинская информация игрока. Справки, если будут, привяжем сюда же.
    """
    anamnesis = ForeignKey(
        to=Anamnesis,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Диагноз',
    )
    respiratory_failure = ForeignKey(
        to=RespiratoryFailure,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Класс ХДН',
    )
    is_confirmed = BooleanField(
        default=False,
        verbose_name='Класс ХДН подтверждён перманентно',
    )
    revision = CharField(
        verbose_name='Пересмотр класса ХДН',
        blank=True,
        null=True,
    )
    wheelchair = BooleanField(
        default=False,
        verbose_name='На коляске'
    )


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
    health_card = OneToOneField(
        to=HealthCard,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Медицинские данные',
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
        constraints = [
            UniqueConstraint(
                name='player_unique',
                fields=['name', 'surname', 'patronymic', 'birth_date'],
            )
        ]


class PlayerTeam(Model):
    """
    Связь "многие ко многим" игрока с командой с добавлением данных игрока
    в этой команде.
    """
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
        to=PlayerPosition,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Позиция игрока',
    )
    role = ForeignKey(
        to=PlayerRole,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Статус игрока',
    )
    number = CharField(
        verbose_name='Игровой номер',
    )


class Coach(BasePerson):
    """
    Тренер команды
    """
    position = ForeignKey(
        to=CoachPosition,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Должность тренера',
    )
    qualification = ForeignKey(
        to=CoachQualification,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Квалификационная категория тренера',
    )
    team = ManyToManyField(
        to=Team,
        through='CoachTeam',
        verbose_name='Команда'
    )

    class Meta(BasePerson.Meta):
        default_related_name = 'coaches'
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'


class CoachTeam(Model):
    """
    Связь "многие ко многим" тренера с командой.
    """
    coach = ForeignKey(
        to=Coach,
        related_name='teams',
        on_delete=CASCADE,
        verbose_name='Игрок',

    )
    team = ForeignKey(
        to=Team,
        related_name='coaches',
        on_delete=CASCADE,
        verbose_name='Команда',
    )
    position = ForeignKey(
        to=CoachPosition,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        verbose_name='Должность тренера',
    )
