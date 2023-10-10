from dataclasses import dataclass
from datetime import date


@dataclass
class BaseUserInfo:
    """Основной класс с обязательными полями.
    """
    name: str
    surname: str
    date_of_birth: date


@dataclass
class FromDocxAdditionalUserInfo(BaseUserInfo):
    """Класс с необязательными полями из документов формата docx.
    """
    birth_certificate: str = None
    passport: str = None
    position: str = None
    player_number: int = None
    is_assistant: bool = False
    is_captain: bool = False
