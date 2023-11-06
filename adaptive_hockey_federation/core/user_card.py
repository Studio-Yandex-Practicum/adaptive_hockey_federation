from dataclasses import dataclass
from datetime import date
from typing import Optional, Union


@dataclass
class BaseUserInfo:
    """Основной класс с обязательными полями.
    """
    name: Union[str, None]
    surname: Union[str, None]
    date_of_birth: Union[date, None]
    team: Union[str, None]
    player_number: int
    position: str


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
class ExcelData(BaseUserInfo):
    """Класс с необязательными полями из таблицы
       "Реестр классов ХДН.xlsx".
    """
    classification: Union[float, None]
    numeric_status: Optional[int] = None
