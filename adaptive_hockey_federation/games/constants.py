"""Константы, используемые в модуле games."""

from enum import StrEnum, IntEnum

TITLE_MAPPING = dict(
    GameCreateView="Создание игры",
    GameEditView="Редактирование игры",
)


class Errors(StrEnum):
    """Константы для сообщений об ошибках."""

    NO_MORE_THAN_TWO_TEAMS_IN_GAME = (
        "В игре может участвовать не более двух команд!"
    )
    MUST_BE_TWO_TEAMS_IN_A_GAME = "В игре должны участвовать две команды!"
    CANNOT_PLAY_AGAINST_SELF = "Команда не может играть с самой собой!"
    INCORRECT_GAME_TEAMS = "Неверный список команд!"
    PERMISSION_MISSING = "Отсутствует разрешение на {action}."
    EDIT_GAME = "редактирование игры"
    CREATE_GAME = "создание игры"
    LIST_VIEW = "просмотр списка игр"


class Literals(StrEnum):
    """Константы для информационных и прочих текстовых сообщений."""

    PARTICIPATING_TEAMS = "Команды, участвующие в игре"
    AVAILABLE_TEAMS = "Команды, доступные для участия в игре"
    TEAMS = "Команды"
    CHOSEN_TEAMS = "Выбранные команды"
    FORM_DATETIME_PLACEHOLDER = "Введите дату проведения игры"
    GAME_NUMBER = "Nr."
    GAME_NAME = "Название"
    VIDEO_LINK = "Ссылка на видео"
    FIRST_TEAM = "Команда 1"
    SECOND_TEAM = "Команда 2"


class Values(IntEnum):
    """Константы для цифровых значений."""

    MIN_PLAYER_NUMBER = 0
    MAX_PLAYER_NUMBER = 99
    MAX_TEAMS_IN_GAME = 2
    PAGINATION_BASE_VALUE = 10
