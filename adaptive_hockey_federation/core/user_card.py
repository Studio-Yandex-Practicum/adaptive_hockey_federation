from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class BaseUserInfo:
    """Основной класс с обязательными полями.
    """
    name: str
    surname: str
    date_of_birth: date
    team: str


@dataclass
class HockeyData(BaseUserInfo):
    """Класс с необязательными полями из документов формата docx.
    """
    patronymic: Optional[str]
    birth_certificate: Optional[str]
    passport: Optional[str]
    position: Optional[str]
    player_number: Optional[int]
    is_assistant: bool = False
    is_captain: bool = False
