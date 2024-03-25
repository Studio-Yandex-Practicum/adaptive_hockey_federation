# constants for users/models.py
NAME_MAX_LENGTH = 256
EMAIL_MAX_LENGTH = 256
QUERY_SET_LENGTH = 15

ROLE_AGENT = "Представитель команды"
ROLE_MODERATOR = "Модератор"
ROLE_ADMIN = "Администратор"
ROLE_SUPERUSER = "admin"
ROLES_CHOICES = (
    (ROLE_AGENT, "Представитель команды"),
    (ROLE_MODERATOR, "Модератор"),
    (ROLE_ADMIN, "Администратор"),
    (ROLE_SUPERUSER, "Суперпользователь"),
)

GROUP_ADMINS = "Администраторы"
GROUP_MODERATORS = "Модераторы"
GROUP_AGENTS = "Представители команд"

GROUPS_BY_ROLE = {
    ROLE_ADMIN: GROUP_ADMINS,
    ROLE_AGENT: GROUP_AGENTS,
    ROLE_MODERATOR: GROUP_MODERATORS,
    ROLE_SUPERUSER: GROUP_ADMINS,
}

# constants for main/models.py
CHAR_FIELD_LENGTH = 256
EMPTY_VALUE_DISPLAY = ""
CLASS_FIELD_LENGTH = 10
DEFAULT_VALUE = 0

MAN = "Мужской"
WOMAN = "Женский"
GENDER_CHOICES = (
    (MAN, "Мужской"),
    (WOMAN, "Женский"),
)

STRIKER = "Нападающий"
BOBBER = "Поплавок"
GOALKEEPER = "Вратарь"
DEFENDER = "Защитник"
PLAYER_POSITION_CHOICES = (
    (STRIKER, "Нападающий"),
    (BOBBER, "Поплавок"),
    (GOALKEEPER, "Вратарь"),
    (DEFENDER, "Защитник"),
)

TRAINER = "тренер"
OTHER = "пушер-тьютор"
STAFF_POSITION_CHOICES = (
    (TRAINER, "тренер"),
    (OTHER, "пушер-тьютор"),
)

TIME_FORMAT = "%H-%M-%S"

MIN_AGE_PlAYER: int = 6
MAX_AGE_PlAYER: int = 18

FORM_HELP_TEXTS = {

    "identity_document": (
        "Введите данные в формате 'Паспорт ХХХХ ХХХХХХ' или "
        "'Свидетельство о рождении X-XX XXXXXX'"
    ),
    "birthday":
    (
        f"Возраст должен быть от {MIN_AGE_PlAYER} до {MAX_AGE_PlAYER} лет"
    ),
    "team": (
        "Список доступных команд, действующие команды обозначены голубым"
        "цветом, чтобы выбрать или удалить зажмите ctrl"
    ),
}
