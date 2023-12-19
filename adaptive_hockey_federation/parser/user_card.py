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
    player_number: Union[int, None]
    position: Union[str, None]
    numeric_status: Union[int, None]
    patronymic: Union[str, None] = None
    birth_certificate: Union[str, None] = None
    passport: Union[str, None] = None
    classification: Union[float, None] = None
    revision: Union[str, None] = None
    is_assistant: bool = False
    is_captain: bool = False

    def __eq__(self, other):
        return all(
            getattr(self, attr) == getattr(other, attr) for attr in vars(self)
        )

    def __hash__(self):
        return hash(
            (
                self.name,
                self.surname,
                self.date_of_birth,
                self.team,
                self.player_number,
                self.position,
                self.numeric_status,
                self.patronymic,
                self.birth_certificate,
                self.passport,
                self.classification,
                self.revision,
                self.is_assistant,
                self.is_captain,

            )
        )
