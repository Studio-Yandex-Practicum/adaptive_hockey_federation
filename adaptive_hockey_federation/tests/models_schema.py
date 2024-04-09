from core.constants import ROLE_AGENT, ROLE_SUPERUSER
from main.models import (
    City,
    Diagnosis,
    Discipline,
    DisciplineLevel,
    DisciplineName,
    Nosology,
    StaffMember,
)

CORRECT_CREATE = "correct_create"
CORRECT_UPDATE = "correct_update"


def get_range_string(start_symbol: str, end_symbol: str) -> str:
    return "".join(
        [chr(i) for i in range(ord(start_symbol), ord(end_symbol) + 1)]
    )


# Типичные валидации

# Используйте кортеж для тестирования строковых полей на каждый элемент
# последовательности поочередно.
RUS_STRINGS = get_range_string("а", "я") + "ё"
RUS_CAPS = RUS_STRINGS.upper()
LATIN_STRINGS = get_range_string("a", "z")
LATIN_CAPS = LATIN_STRINGS.upper()
ALL_LETTERS = (
    (RUS_STRINGS, RUS_CAPS, LATIN_STRINGS, LATIN_CAPS),
    "любые буквы русского и (или) латинского алфавита",
)
ALL_RUS_LETTERS_IN_FIO = (
    RUS_STRINGS.capitalize(),
    "любые буквы русского алфавита",
)
VERY_LONG_TEXT = "Lorem ipsum dolor sit amet... Съешь еще этих мягких " * 1000
ALL_LOWER = ("василий", "начало со строчной буквы")
ALL_CAPS = ("ВАСИЛИЙ", "строка полностью из прописных букв")
SPACES = ("Салтыков Щедрин", "наличие хотя бы одного пробела")
TWO_OR_MORE_SPACES = ("Алибаба олгы моглы", "наличие двух и более пробелов")
DOUBLE_LAST_NAME = ("Петров-Водкин", "двойная фамилия через дефис")
LOWER_SECOND_LAST_NAME = ("Петров-водкин", "вторая фамилия со строчной буквы")
DOUBLE_PATRONYMIC = ("Алимамбек оглы", "двойное отчество через пробел")
MIDDLE_CAP = ("ВаСилий", "прописная буква не в начале слова")
NOT_CYR = ("Gennadiy", "некириллические символы")
FIGURES_AND_LETTERS = ("Пётр1", "цифры наряду с буквами")
LONGER_THEN_256 = (("а" * 257).capitalize(), "строка длиннее 256 символов")
LONGER_THEN_150 = (("а" * 151).capitalize(), "строка длиннее 150 символов")
LONG_256 = (("а" * 256).capitalize(), "строка длиной до 256 символов")
LONG_150 = (("а" * 150).capitalize(), "строка длиной до 150 символов")
FIGURES_ONLY = ("1234567890", "значение, состоящее только из " "цифр")
INTEGER = (1, "числовое значение поля")
FLOAT = (1.25, "дробное значение поля")
ZERO = (0, "нулевое значение поля")
NEGATIVE = (-1, "отрицательное значение поля")
NONE = (None, "пустое значение поля")
NULL = ("", "значение поля, состоящее из пустой строки")
PUNCTUATION_MARKS_EXCEPT_HYPHEN = (
    "Васи",
    tuple("~@#$%^&*()`.,\\{}\"[]<>/*+:;|!№?='"),
    "лий",
    "наличие символов пунктуации",
)
PUNCTUATION_MARKS = (
    "Васи",
    tuple("-~@#$%^&*()`.,\\{}\"[]<>/*+:;|!№?='"),
    "лий",
    "наличие символов пунктуации",
)
PUNCTUATION_MARKS_ONLY = (
    '!"№;%:?()_',
    "строка, состоящая только из знаков препинания",
)
SPACES_ONLY = ("    ", "строка, состоящая из одних пробелов")

THE_ONLY_LETTER = (tuple("ФFгg"), "строка, состоящая из единственной буквы")

THE_ONLY_CYR_LETTER = (
    tuple("АБЯЁ"),
    "строка, состоящая из одной русской буквы",
)

THE_ONLY_LATIN_LETTER = (
    tuple("ABYZ"),
    "строка, состоящая из одной латинской буквы",
)

INCORRECT_EMAIL = (
    "",
    ("adfasdf.lkj", "неправ@иль.но", "дажеблизконеемайл"),
    "",
    "невалидный адрес электронной почты",
)
UNFORESEEN_ROLE = ("Повелительмух", "непредусмотренная роль пользователя")
INCORRECT_PHONE = (
    (
        "+7 5f5 555 55 55",
        "+7 555 555-55-55",
        "+7 5555 555 55 55",
        "+7 555 5555 55 55",
        "+6 555 555 55 55",
        "-7 555 555 55 55",
        "+7_555_555 55 55",
        "+7 xxx xxx xx xx",
        "+Д 555 555 55 55",
        "+А БРА КАД-АБ-РА",
        "8_926_555@ya.ya",
        "8_926_555@55.55",
    ),
    "номер телефона в неверном формате",
)
CORRECT_PHONE = (
    (
        "+7 955 555-55-54",
        "+7 900 000-00-00",
        "+7 959 111-11-11",
        "+7 987 654-32-10",
    ),
    "правильный номер телефона",
)
CORRECT_CITY_NAMES = (
    (
        "г. Город-через-Дефис",
        "пгт. Поселок Городского Типа",
        "пос. им. В.И. Ленина",
        "Арзамас-16",
    ),
    "сложные топонимы в названии города",
)

INCORRECT_DOC_ID = (
    (
        "Паспорт 30 01 023456",
        "Паспорт АБРА КАДАБР",
        "ПаспАрт 9898 989898",
        "СвидетельствА о рождении I-ML 656565",
        "Абракадабрааб р акадабра I-ML 656565",
        "Свидетельство о брожении I-ML 656565",
    ),
    "неверный формат документа, удостоверяющего личность",
)

CORRECT_DOC_ID = (
    (
        "Паспорт 3001 023456",
        "Свидетельство о рождении I-ML 656565",
        "Свидетельство о рождении II-ML 656565",
    ),
    "документ, удостоверяющий личность, в корректном формате",
)

INCORRECT_GENDER_CHOICE = ("Оно", "некорректный пол")
INCORRECT_PLAYER_POSITION = ("Зритель", "некорректная позиция игрока")

USER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "first_name": "Василий",
        "last_name": "Иванович",
        "patronymic": "Петров",
        "role": ROLE_SUPERUSER,
        "email": "fake@fake.com",
        "phone": "+7 990 060-45-71",
        "is_staff": False,
        "password": "pAss9742!word",
    },
    CORRECT_UPDATE: {
        "first_name": "Бурямглоюнебокроетвихриснежныекрутятокакзверьоназавоет",
        "last_name": "Съешьещеэтихмягкихфранцузскихбулочекдавыпейчаюев",
        "patronymic": "Кракозябробормоглототроглодитобрандашмыгович",
        "role": ROLE_AGENT,
        "email": "fake@fake.com",
        "phone": "+7 990 060-45-72",
        "is_staff": False,
        "password": "NewPAss9742!word",
    },
    "must_not_be_admitted": (
        {
            "fields": ("first_name", "last_name", "patronymic"),
            "test_values": (
                ALL_LOWER,
                ALL_CAPS,
                MIDDLE_CAP,
                NOT_CYR,
                FIGURES_AND_LETTERS,
                LONGER_THEN_256,
                PUNCTUATION_MARKS_EXCEPT_HYPHEN,
            ),
        },
        {
            "fields": (
                "first_name",
                "last_name",
            ),
            "test_values": (NULL,),
        },
        {
            "fields": "last_name",
            "test_values": (LOWER_SECOND_LAST_NAME, SPACES),
        },
        {"fields": "patronymic", "test_values": (TWO_OR_MORE_SPACES,)},
        {"fields": "email", "test_values": (INCORRECT_EMAIL,)},
        {"fields": "role", "test_values": (UNFORESEEN_ROLE,)},
        {"fields": "phone", "test_values": (INCORRECT_PHONE,)},
    ),
    "must_be_admitted": (
        {
            "fields": ("last_name", "first_name", "patronymic"),
            "test_values": (THE_ONLY_CYR_LETTER,),
        },
        {"fields": "last_name", "test_values": (DOUBLE_LAST_NAME,)},
        {"fields": "patronymic", "test_values": (DOUBLE_PATRONYMIC,)},
        {"fields": "phone", "test_values": (CORRECT_PHONE,)},
    ),
}

GROUP_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Группа в полосатых купальниках",
    },
    CORRECT_UPDATE: {
        "name": "Группа крови на рукаве",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_150,
                NULL,
            ),
        },
    ),
    "must_be_admitted": ({"fields": "name", "test_values": (LONG_150,)},),
}

CITY_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Городкоторогонет",
    },
    CORRECT_UPDATE: {
        "name": "Новыйгородкоторогонет",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                NOT_CYR,
                FIGURES_ONLY,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (LONG_256, FIGURES_AND_LETTERS, CORRECT_CITY_NAMES),
        },
    ),
}

DIAGNOSIS_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Диагнозкоторогонет",
        "nosology": Nosology,
    },
    CORRECT_UPDATE: {
        "name": "Новыйдиагнозкоторогонет",
        "nosology": Nosology,
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                FIGURES_ONLY,
                PUNCTUATION_MARKS_ONLY,
                THE_ONLY_LETTER,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONG_256,
                FIGURES_AND_LETTERS,
            ),
        },
    ),
}

SIMPLE_UNIQUE_NAME_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Какоетоимя",
    },
    CORRECT_UPDATE: {
        "name": "Какоетоновоеимя",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                FIGURES_ONLY,
                PUNCTUATION_MARKS_ONLY,
                THE_ONLY_LETTER,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONG_256,
                FIGURES_AND_LETTERS,
                ALL_LETTERS,
            ),
        },
    ),
}


NOSOLOGY_MODEL_TEST_SCHEMA = SIMPLE_UNIQUE_NAME_MODEL_TEST_SCHEMA

DISCIPLINE_NAME_MODEL_TEST_SCHEMA = SIMPLE_UNIQUE_NAME_MODEL_TEST_SCHEMA

DISCIPLINE_LEVEL_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Наименование дисциплины или статуса дисциплины",
    },
    CORRECT_UPDATE: {
        "name": "Новое наименование дисциплины или статуса дисциплины",
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONGER_THEN_256,
                NULL,
                PUNCTUATION_MARKS_ONLY,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                LONG_256,
                FIGURES_AND_LETTERS,
                ALL_LETTERS,
            ),
        },
    ),
}

DISCIPLINE_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "discipline_name": DisciplineName,
        "discipline_level": DisciplineLevel,
    },
    CORRECT_UPDATE: {
        "discipline_name": DisciplineName,
        "discipline_level": DisciplineLevel,
    },
}

STAFF_MEMBER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Василий",
        "surname": "Иванович",
        "patronymic": "Петров",
        "phone": "+7 990 060-45-71",
    },
    CORRECT_UPDATE: {
        "name": "Бурямглоюнебокроетвихриснежныекрутятокакзверьоназавоет",
        "surname": "Съешьещеэтихмягкихфранцузскихбулочекдавыпейчаюев",
        "patronymic": "Кракозябробормоглототроглодитобрандашмыгович",
        "phone": "+7 990 060-45-72",
    },
    "must_not_be_admitted": (
        {
            "fields": ("name", "surname", "patronymic"),
            "test_values": (
                ALL_LOWER,
                ALL_CAPS,
                MIDDLE_CAP,
                NOT_CYR,
                FIGURES_AND_LETTERS,
                LONGER_THEN_256,
                PUNCTUATION_MARKS_EXCEPT_HYPHEN,
            ),
        },
        {
            "fields": (
                "name",
                "surname",
            ),
            "test_values": (NULL,),
        },
        {
            "fields": "surname",
            "test_values": (LOWER_SECOND_LAST_NAME, SPACES),
        },
        {"fields": "patronymic", "test_values": (TWO_OR_MORE_SPACES,)},
        {"fields": "phone", "test_values": (INCORRECT_PHONE,)},
    ),
    "must_be_admitted": (
        {
            "fields": ("surname", "name", "patronymic"),
            "test_values": (THE_ONLY_CYR_LETTER,),
        },
        {"fields": "surname", "test_values": (DOUBLE_LAST_NAME,)},
        {"fields": "patronymic", "test_values": (DOUBLE_PATRONYMIC,)},
        {"fields": "phone", "test_values": (CORRECT_PHONE,)},
    ),
}

STAFF_TEAM_MEMBER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "staff_member": StaffMember,
        "staff_position": "тренер",
        "qualification": "Какаятотамквалификация",
        "notes": "Наш величайший тренер родился еще в те времена, когда...",
    },
    CORRECT_UPDATE: {
        "staff_member": StaffMember,
        "staff_position": "пушер-тьютор",
        "qualification": "Какаятотамещеквалификация",
        "notes": "Этот пушер-тьютор толкает игроков на лед с такой силой...",
    },
    "must_not_be_admitted": (
        {
            "fields": "staff_position",
            "test_values": (
                ("повелительмух", "непредусмотренная позиция сотрудника"),
                NULL,
            ),
        },
        {
            "fields": "qualification",
            "test_values": (LONGER_THEN_256,),
        },
    ),
    "must_be_admitted": (
        {"fields": "qualification", "test_values": (THE_ONLY_LETTER,)},
    ),
}

TEAM_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Команда молодости нашей",
        "city": City,
        "discipline_name": DisciplineName,
    },
    CORRECT_UPDATE: {
        "name": "Команда мечты",
        "city": City,
        "discipline_name": DisciplineName,
    },
    "must_not_be_admitted": (
        {
            "fields": "name",
            "test_values": (
                NULL,
                PUNCTUATION_MARKS_ONLY,
                FIGURES_ONLY,
                THE_ONLY_LETTER,
            ),
        },
    ),
    "must_be_admitted": (
        {
            "fields": "name",
            "test_values": (ALL_LETTERS, FIGURES_AND_LETTERS, SPACES),
        },
    ),
}

PLAYER_MODEL_TEST_SCHEMA = {
    CORRECT_CREATE: {
        "name": "Василий",
        "surname": "Иванович",
        "patronymic": "Петров",
        "diagnosis": Diagnosis,
        "discipline": Discipline,
        "birthday": "2010-03-25",
        "gender": "Мужской",
        "level_revision": "Тестовый уровень ревизии.",
        "position": "Поплавок",
        "number": 45,
        "is_captain": False,
        "is_assistent": False,
        "identity_document": "Паспорт 3030 303030",
    },
    CORRECT_UPDATE: {
        "name": "Бурямглоюнебокроетвихриснежныекрутятокакзверьоназавоет",
        "surname": "Съешьещеэтихмягкихфранцузскихбулочекдавыпейчаюев",
        "patronymic": "Кракозябробормоглототроглодитобрандашмыгович",
        "diagnosis": Diagnosis,
        "discipline": Discipline,
        "birthday": "2009-03-25",
        "gender": "Женский",
        "level_revision": "Какой-то другой тестовый уровень ревизии.",
        "position": "Нападающий",
        "number": 41,
        "is_captain": True,
        "is_assistent": True,
        "identity_document": "Паспорт 4040 404040",
    },
    "must_not_be_admitted": (
        {
            "fields": ("name", "surname", "patronymic"),
            "test_values": (
                ALL_LOWER,
                ALL_CAPS,
                MIDDLE_CAP,
                NOT_CYR,
                FIGURES_AND_LETTERS,
                LONGER_THEN_256,
                PUNCTUATION_MARKS_EXCEPT_HYPHEN,
            ),
        },
        {
            "fields": (
                "name",
                "surname",
            ),
            "test_values": (NULL,),
        },
        {
            "fields": "surname",
            "test_values": (LOWER_SECOND_LAST_NAME, SPACES),
        },
        {"fields": "patronymic", "test_values": (TWO_OR_MORE_SPACES,)},
        {"fields": "identity_document", "test_values": (INCORRECT_DOC_ID,)},
        {"fields": "gender", "test_values": (INCORRECT_GENDER_CHOICE,)},
        {"fields": "position", "test_values": (INCORRECT_PLAYER_POSITION,)},
        {"fields": "number", "test_values": (NEGATIVE,)},
    ),
    "must_be_admitted": (
        {
            "fields": ("surname", "name", "patronymic"),
            "test_values": (THE_ONLY_CYR_LETTER, ALL_RUS_LETTERS_IN_FIO),
        },
        {"fields": "surname", "test_values": (DOUBLE_LAST_NAME,)},
        {"fields": "patronymic", "test_values": (DOUBLE_PATRONYMIC,)},
        {"fields": "identity_document", "test_values": (CORRECT_DOC_ID,)},
    ),
}
