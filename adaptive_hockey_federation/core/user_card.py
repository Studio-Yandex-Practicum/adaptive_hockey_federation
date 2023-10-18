from dataclasses import dataclass
from datetime import date


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
    patronymic: str = None
    birth_certificate: str = None
    passport: str = None
    position: str = None
    player_number: int = None
    is_assistant: bool = False
    is_captain: bool = False


@dataclass
class ExcelDataPlayer_1(BaseUserInfo):
    """Класс с необязательными полями из документов формата xlsx.
    """
    position: str = None
    classification: str = None


@dataclass
class ExcelDataCoach_1:
    """Класс с необязательными полями из документов формата xlsx.
    """
    name: str
    surname: str
    team: str
    role: str = None


@dataclass
class ExcelData_2(BaseUserInfo):
    """Класс с необязательными полями из документов формата xlsx.
    """
    classification: str
    riding_face_forward: int = None
    riding_backwards: int = None
    cast: int = None
    dribbling: int = None
    team_hockey: int = None
    result: float = None


@dataclass
class ExcelDataFirstSheet_2(BaseUserInfo):
    """Класс с необязательными полями из документов формата xlsx.
    """
    classification: str
    revision: int
