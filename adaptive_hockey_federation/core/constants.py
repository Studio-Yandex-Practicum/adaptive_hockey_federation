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
GROUP_SUPERUSER = "Суперпользователь"

GROUPS_BY_ROLE = {
    ROLE_ADMIN: GROUP_ADMINS,
    ROLE_AGENT: GROUP_AGENTS,
    ROLE_MODERATOR: GROUP_MODERATORS,
    ROLE_SUPERUSER: GROUP_SUPERUSER,  # superuser
}

# constants for main/models.py
CHAR_FIELD_LENGTH = 256
EMPTY_VALUE_DISPLAY = ""
CLASS_FIELD_LENGTH = 10
DEFAULT_VALUE = 0

GENDER_CHOICES = (
    ("male", "Мужской"),
    ("female", "Женский"),
)

PLAYER_POSITION_CHOICES = (
    ("striker", "Нападающий"),
    ("bobber", "Поплавок"),
    ("goalkeeper", "Вратарь"),
    ("defender", "Защитник"),
)

STAFF_POSITION_CHOICES = (
    ("trainer", "тренер"),
    ("other", "пушер-тьютор"),
)

TIME_FORMAT = "%H-%M-%S"
