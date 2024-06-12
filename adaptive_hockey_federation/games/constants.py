"""Константы, используемые в модуле games."""

from enum import IntEnum, StrEnum

GAME_TITLE_MAPPING = dict(
    GameCreateView="Создание игры",
    GameEditView="Редактирование игры",
)


class Errors(StrEnum):
    """Константы для сообщений об ошибках."""

    NO_MORE_THAN_TWO_TEAMS_IN_GAME = (
        "В игре может участвовать не более двух команд!"
    )
    MUST_BE_TWO_TEAMS_IN_A_GAME = "В игре должны участвовать две команды!"
    CANNOT_PLAY_GAME_AGAINST_SELF = "Команда не может играть с самой собой!"
    INCORRECT_GAME_TEAMS = "Неверный список команд!"
    PERMISSION_MISSING = "Отсутствует разрешение на {action}."
    EDIT_GAME = "редактирование игры"
    EDIT_PLAYER_NUMBER = "редактирование номеров игроков"
    CREATE_GAME = "создание игры"
    DELETE_GAME = "удаление игры"
    GAME_LIST_VIEW = "просмотр списка игр"


class Literals(StrEnum):
    """Константы для информационных и прочих текстовых сообщений."""

    GAME_PARTICIPATING_TEAMS = "Команды, участвующие в игре"
    GAME_AVAILABLE_TEAMS = "Команды, доступные для участия в игре"
    GAME_TEAMS = "Команды"
    GAME_CHOSEN_TEAMS = "Выбранные команды"
    GAME_FORM_DATETIME_PLACEHOLDER = "Введите дату проведения игры"
    GAME_NUMBER = "Nr."
    GAME_NAME = "Название"
    GAME_VIDEO_LINK = "Ссылка на видео"
    GAME_FIRST_TEAM = "Команда 1"
    GAME_SECOND_TEAM = "Команда 2"


class NumericalValues(IntEnum):
    """Константы для цифровых значений."""

    GAME_MIN_PLAYER_NUMBER = 0
    GAME_MAX_PLAYER_NUMBER = 99
    MAX_TEAMS_IN_GAME = 2
    PAGINATION_BASE_VALUE = 10
