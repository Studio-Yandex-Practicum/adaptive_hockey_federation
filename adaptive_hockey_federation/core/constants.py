# constants for users/models.py
import datetime

NAME_MAX_LENGTH = 256
EMAIL_MAX_LENGTH = 256
QUERY_SET_LENGTH = 15

ROLE_AGENT = "agent"
ROLE_MODERATOR = "moderator"
ROLE_ADMIN = "admin"
ROLES_CHOICES = (
    (ROLE_AGENT, "Представитель команды"),
    (ROLE_MODERATOR, "Модератор"),
    (ROLE_ADMIN, "Администратор"),
)

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
    ("other", "другой"),
)

TIME_FORMAT = "%H-%M-%S"

TIMESPAN_CHOICES = (
    (datetime.datetime.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    ), "Текущий месяц"),
    (datetime.datetime.now().replace(
        month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    ), "Текущий год"),
)

BLANK_CHOICE = [(None, 'Все')]
