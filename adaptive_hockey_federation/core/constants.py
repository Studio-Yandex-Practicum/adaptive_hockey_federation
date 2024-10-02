from dataclasses import dataclass
from enum import IntEnum, StrEnum


class UserConstans(IntEnum):
    """Константы для приложения users."""

    NAME_MAX_LENGTH = 256
    EMAIL_MAX_LENGTH = 256
    QUERY_SET_LENGTH = 15


class Role(StrEnum):
    """Роли пользователей."""

    AGENT = "Представитель команды"
    MODERATOR = "Модератор"
    ADMIN = "Администратор"
    SUPERUSER = "Администратор"


ROLES_CHOICES = (
    (Role.AGENT, "Представитель команды"),
    (Role.MODERATOR, "Модератор"),
    (Role.ADMIN, "Администратор"),
)


class Group(StrEnum):
    """Группы ролей пользоватлей."""

    ADMINS = "Администраторы"
    MODERATORS = "Модераторы"
    AGENTS = "Представители команд"


GROUPS_BY_ROLE = {
    Role.ADMIN: Group.ADMINS,
    Role.AGENT: Group.AGENTS,
    Role.MODERATOR: Group.MODERATORS,
    Role.SUPERUSER: Group.ADMINS,
}


class Discipline(StrEnum):
    """Виды дисциплин в хоккее."""

    SLEDGE_HOCKEY = "Следж-хоккей"
    BLIND_HOCKEY = "Хоккей для незрячих"
    SPECIAL_HOCKEY = "Специальный хоккей"
    ROLLER_HOCKEY = "Роликовый следж-хоккей"


DISCIPLINE_LEVELS = {
    Discipline.SLEDGE_HOCKEY: (1, 2, 3, 4, 5, 6),
    Discipline.ROLLER_HOCKEY: (1, 2, 3, 4, 5, 6),
    Discipline.BLIND_HOCKEY: ("B1", "B2", "B3", "B4", "B5", "б/к"),
    Discipline.SPECIAL_HOCKEY: ("A", "B", "C"),
}


class MainConstantsInt(IntEnum):
    """Константы int для main/models.py."""

    CHAR_FIELD_LENGTH = 256
    CLASS_FIELD_LENGTH = 10
    DEFAULT_VALUE = 0


class MainConstantsStr(StrEnum):
    """Константы str для main/models.py."""

    EMPTY_VALUE_DISPLAY = ""


class Gender(StrEnum):
    """Пол."""

    MAN = "Мужской"
    WOMAN = "Женский"


GENDER_CHOICES = (
    (Gender.MAN.value, "Мужской"),
    (Gender.WOMAN.value, "Женский"),
)


class PlayerPosition(StrEnum):
    """Позиции игроков."""

    STRIKER = "Нападающий"
    BOBBER = "Поплавок"
    GOALKEEPER = "Вратарь"
    DEFENDER = "Защитник"


PLAYER_POSITION_CHOICES = (
    (PlayerPosition.STRIKER.value, "Нападающий"),
    (PlayerPosition.BOBBER.value, "Поплавок"),
    (PlayerPosition.GOALKEEPER.value, "Вратарь"),
    (PlayerPosition.DEFENDER.value, "Защитник"),
)


class StaffPosition(StrEnum):
    """Роли представителей команд."""

    TRAINER = "тренер"
    OTHER = "пушер-тьютор"


STAFF_POSITION_CHOICES = (
    (StaffPosition.TRAINER.value, "тренер"),
    (StaffPosition.OTHER.value, "пушер-тьютор"),
)


class TimeFormat:
    """Форматы времени."""

    TIME_FORMAT = "%H-%M-%S"


class AgeLimits(IntEnum):
    """Возростные лимиты."""

    MIN_AGE_PLAYER = 6
    MAX_AGE_PLAYER = 18


FORM_HELP_TEXTS = {
    "identity_document": (
        "Введите данные в формате 'Паспорт ХХХХ ХХХХХХ' или "
        "'Свидетельство о рождении X-XX XXXXXX'"
    ),
    "birthday": (
        f"Возраст должен быть от {AgeLimits.MIN_AGE_PLAYER}"
        f"до {AgeLimits.MAX_AGE_PLAYER} лет"
    ),
    "available_teams": ("Список доступных команд перемещение двойным щелчком"),
    "email": (
        "Введите актуальную электронную почту в формате example@domen.ru"
    ),
    "role": ("Выберите роль которая соответствует пользователю"),
    "player_teams": (
        "Список команд в которых состоит игрок удаление двойным щелчком"
    ),
    "staff_teams": (
        "Список команд в которых состоит сотрудник удаление двойным щелчком"
    ),
    "available_disciplines": (
        "Список доступных дисциплин перемещение двойным щелчком"
    ),
    "disciplines": "Список дисциплин в соревновании",
}


@dataclass
class FileConstants:
    """Константы для файлов."""

    FILE_RESOLUTION = ("png", "jpeg", "jpg", "pdf")
    MAX_UPLOAD_SIZE: int = 10485760
    MAX_UPLOAD_SIZE_MB: str = str(int(MAX_UPLOAD_SIZE / (1024 * 1024))) + " MB"


SEARCH_ALIAS = {
    "surname": "surname",
    "name": "name",
    "birthday": "birthday",
    "gender": "gender",
    "number": "surname",
    "discipline": "discipline__discipline_name_id__name",
    "diagnosis": "diagnosis__name",
    "city": "city_name",
}


class Directory:
    """Директории."""

    GAMES = "games"
    PLAYER_VIDEO_DIR = "player_video"
    UNLOAD_DIR = "unloads_data"


class YadiskDirectory(StrEnum):
    """Директории на Яндекс.Диске."""

    GAMES = "games"
    PLAYER_GAMES = "player_games"


PLAYER_GAME_NAME = "{surname}_{name[0]}_{patronymic[0]}_{game_name}.mp4"
