import openpyxl

from adaptive_hockey_federation.core.user_card import BaseUserInfo


def xlsx_parser(path: str) -> list[BaseUserInfo]:
    """Функция парсит xlsx файлы и возвращает
    игроков в виде dataclass ExcelData.
    """
    players = []
    sheet_data = []
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    header = [cell.value for cell in sheet[1]]  # type: ignore
    for row in sheet.iter_rows(min_row=2, values_only=True):  # type: ignore
        sheet_data.append(dict(zip(header, row)))
    for data in sheet_data:
        if data.get('ФИО игрока') is not None:
            player = BaseUserInfo(
                team=data.get('Команда'),
                name=data.get('ФИО игрока').split()[0],  # type: ignore
                surname=data.get('ФИО игрока').split()[1],  # type: ignore
                date_of_birth=data.get('Дата рождения'),
                player_number=data.get('Номер игрока'),
                position=data.get('Позиция'),
                classification=data.get('Класс'),
                revision=data.get('Пересмотр (начало сезона)'),
                numeric_status=None
            )
            players.append(player)
    return players
