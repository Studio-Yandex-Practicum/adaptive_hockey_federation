# constants for users/models.py
NAME_MAX_LENGTH = 256
EMAIL_MAX_LENGTH = 256
QUERY_SET_LENGTH = 15

ROLE_AGENT = "Представитель команды"
ROLE_MODERATOR = "Модератор"
ROLE_ADMIN = "Администратор"
ROLE_SUPERUSER = "Администратор"
ROLES_CHOICES = (
    (ROLE_AGENT, "Представитель команды"),
    (ROLE_MODERATOR, "Модератор"),
    (ROLE_ADMIN, "Администратор"),
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

# Виды дисциплин в хоккее
SLEDGE_HOCKEY = "Следж-хоккей"
BLIND_HOCKEY = "Хоккей для незрячих"
SPECIAL_HOCKEY = "Специальный хоккей"
ROLLER_HOCKEY = "Роликовый следж-хоккей"

DISCIPLINE_LEVELS = {
    SLEDGE_HOCKEY: (1, 2, 3, 4, 5, 6),
    ROLLER_HOCKEY: (1, 2, 3, 4, 5, 6),
    BLIND_HOCKEY: ("B1", "B2", "B3", "B4", "B5", "б/к"),
    SPECIAL_HOCKEY: ("A", "B", "C"),
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
    "birthday": (
        f"Возраст должен быть от {MIN_AGE_PlAYER} до {MAX_AGE_PlAYER} лет"
    ),
    "available_teams": ("Список доступных команд перемещение двойным щелчком"),
    "email": (
        "Введите актуальную электронную почту" " в формате example@domen.ru"
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
    "video_frame_info": "Введите информацию в формате json"
}

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

UNLOAD_DIR = "unloads_data"
