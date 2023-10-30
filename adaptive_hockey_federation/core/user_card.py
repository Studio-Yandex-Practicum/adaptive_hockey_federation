from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class BaseUserInfo:
    """Основной класс с обязательными полями.
    """
    name: str
    surname: str
    patronymic: str
    date_of_birth: date
    team: str
    player_number: int
    position: str


@dataclass
class HockeyData(BaseUserInfo):
    """Класс с необязательными полями из документов формата docx.
    """
    numeric_status: Optional[int] = None
    player_class: Optional[str] = None
