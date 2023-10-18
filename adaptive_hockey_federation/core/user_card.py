from dataclasses import dataclass
from datetime import date
from typing import Union


@dataclass
class BaseUserInfo:
    """Основной класс с обязательными полями.
    """
    name: Union[str, None]
    surname: Union[str, None]
    date_of_birth: Union[date, None]
    team: Union[str, None]


@dataclass
class HockeyData(BaseUserInfo):
    """Класс с необязательными полями из документов формата docx.
    """
    patronymic: Union[str, None]
    birth_certificate: Union[str, None]
    passport: Union[str, None]
    position: Union[str, None]
    player_number: Union[int, None]
    is_assistant: bool = False
    is_captain: bool = False


@dataclass
class ExcelDataPlayer_1(BaseUserInfo):
    """Класс с необязательными полями из таблицы "Состав команды.xlsx".
       Информация об игроках.
    """
    position: Union[str, None]
    classification: Union[str, None]


@dataclass
class ExcelDataCoach_1:
    """Класс с необязательными полями из таблицы "Состав команды.xlsx".
       Информация о руководительском составе.
    """
    name: Union[str, None]
    surname: Union[str, None]
    team: Union[str, None]
    role: Union[str, None]


@dataclass
class ExcelData_2(BaseUserInfo):
    """Класс с необязательными полями из таблицы
       "Копия Сводная таблица по командам с классами ЛТ.xlsx".
       Информация из всех листов, кроме первого
    """
    classification: Union[float, None]
    riding_face_forward: Union[float, None]
    riding_backwards: Union[float, None]
    cast: Union[float, None]
    dribbling: Union[float, None]
    team_hockey: Union[float, None]
    result: Union[float, None]


@dataclass
class ExcelDataFirstSheet_2(BaseUserInfo):
    """Класс с необязательными полями из таблицы
       "Копия Сводная таблица по командам с классами ЛТ.xlsx".
       Информация из первого листа.
    """
    classification: Union[str, None]
    revision: Union[int, None]
