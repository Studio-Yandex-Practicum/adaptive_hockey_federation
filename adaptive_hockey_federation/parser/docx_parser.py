import re
import tempfile
from datetime import date
from urllib.parse import urlencode

import docx
import requests

from adaptive_hockey_federation.core.user_card import HockeyData

NAME = '[И|и][М|м][Я|я]'
SURNAME = '[Ф|ф][А|а][М|м][И|и][Л|л][И|и][Я|я]'
DATE_OF_BIRTH = '[Д|д][А|а][Т|т][А|а]'
TEAM = '[К|к][О|о][М|м][А|а][Н|н][Д|д][А|а]'
PATRONYMIC = '[О|о][Т|т][Ч|ч][Е|е][С|с][Т|т][В|в][О|о]'
BIRTH_CERTIFICATE = '([С|с][В|в].+?[В|в][О|о])|([С|с][В|в]..[О|о].[Р|р])'
PASSPORT = '([П|п][А|а][С|с][П|п][О|о][Р|р][Т|т])'
POSITION = '[П|п][О|о][З|з][И|и][Ц|ц][И|и][Я|я]'
PLAYER_NUMBER = '[И|и][Г|г].+[Н|н][О|о][М|м][Е|е][Р|р]'
ASSISTANT = '[А|а][С|с][С|с][И|и][С|с][Т|т][Е|е][Н|н][Т|т]'
CAPTAIN = '[К|к][А|а][П|п][И|и][Т|т][А|а][Н|н]'

YANDEX_API = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
DOWNLOAD_URL = 'https://disk.yandex.ru/i/ZRusBovQDTl5zw'


def read_file_columns(ya_api: str, download_url: str) -> list[docx]:
    """Функция загружает данные из примера во временный файл,
    находит таблицы в нем и возвращает список объектов
    docx с данными каждого столбца.
    """
    work_url = ya_api + urlencode(dict(public_key=download_url))
    response = requests.get(work_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with tempfile.TemporaryFile() as file:
        file.write(download_response.content)
        document = docx.Document(file)
        file.close()
    all_columns = []
    for table in document.tables:
        for index, column in enumerate(table.columns):
            all_columns.append(column)

    return all_columns


def read_file_text(ya_api: str, download_url: str) -> list[str]:
    """Функция загружает данные из примера во временный файл и
    находит весь текст в нем.
    """
    work_url = ya_api + urlencode(dict(public_key=download_url))
    response = requests.get(work_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with tempfile.TemporaryFile() as file:
        file.write(download_response.content)
        document = docx.Document(file)
        file.close()
    text = []
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            text.append(run.text)

    return text


def columns_parser(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция находит столбец по названию и списком выводит содержимое
    каждой ячейки этого столбца.
    """
    column_data = []
    for column in columns:
        cell_text = list(cell.text for cell in column.cells)
        if re.search(regular_expression, cell_text[0]):
            for text in cell_text[1:]:
                if not text:
                    column_data.append(None)
                else:
                    column_data.append(text)

    return column_data


def find_names(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце имена. Если имя записано
    вместе с фамилией и отчеством, то функция опирается на шаблон ФИО
    (имя идет после фамилии на втором месте).
    """
    names_list = columns_parser(columns, regular_expression)
    names_list_clear = []
    for name in names_list:
        if len(name.split()) > 1:
            names_list_clear.append(name.split()[1])
        else:
            names_list_clear.append(name)

    return names_list_clear


def find_surnames(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце фамилии. Если фамилия записана
    вместе с именем и отчеством, то функция опирается на шаблон ФИО
    (фамилия идет на первом месте).
    """
    surnames_list = columns_parser(columns, regular_expression)
    surnames_list_clear = []
    for surname in surnames_list:
        if len(surname.split()) > 1:
            surnames_list_clear.append(surname.split()[0])
        else:
            surnames_list_clear.append(surname)

    return surnames_list_clear


def find_dates_of_birth(
        columns: list[docx],
        regular_expression: str
) -> list[date]:
    """Функция парсит в искомом столбце дату рождения
    и опирается на шаблон дд.мм.гггг.
    """
    dates_of_birth_list = columns_parser(columns, regular_expression)
    dates_of_birth_list_clear = []
    for date_of_birth in dates_of_birth_list:
        day, month, year = date_of_birth.split('.')
        dates_of_birth_list_clear.append(date(int(year), int(month), int(day)))

    return dates_of_birth_list_clear


def find_team(text: list[str], regular_expression: str) -> str:
    """Функция парсит название команды.
    """
    team = ''
    for index, txt in enumerate(text):
        if re.search(regular_expression, txt):
            team = text[index + 2]

    return team


def find_patronymics(
        columns: list[docx],
        regular_expression: str
) -> list[str]:
    """Функция парсит в искомом столбце отчества. Если отчество записано
    вместе с именем и фамилией, то функция опирается на шаблон ФИО
    (отчество идет на последнем месте).
    """
    patronymics_list = columns_parser(columns, regular_expression)
    patronymics_list_clear = []
    for patronymic in patronymics_list:
        if len(patronymic.split()) > 1:
            patronymics_list_clear.append(patronymic.split()[2])
        else:
            patronymics_list_clear.append(patronymic)

    return patronymics_list_clear


def find_birth_certificates(
        columns: list[docx],
        regular_expression: str
) -> list[str]:
    """Функция парсит в искомом столбце данные свидетельства о рождении.
    """
    birth_certificates_list = columns_parser(columns, regular_expression)
    birth_certificates_list_clear = []
    for birth_certificate in birth_certificates_list:
        if re.search(regular_expression, birth_certificate):
            text = re.sub(regular_expression, '', birth_certificate)
            birth_certificates_list_clear.append(text.replace('\n', ' '))
        else:
            birth_certificates_list_clear.append(None)

    return birth_certificates_list_clear


def find_passports(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце данные паспорта.
    """
    passports_list = columns_parser(columns, regular_expression)
    passports_list_clear = []
    for passport in passports_list:
        if re.search(regular_expression, passport):
            text = re.sub(regular_expression, '', passport)
            passports_list_clear.append(text.replace('\n', ' '))
        else:
            passports_list_clear.append(None)

    return passports_list_clear


def find_positions(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце позицию игрока на поле.
    """
    positions_list = columns_parser(columns, regular_expression)
    positions_list_clear = []
    for position in positions_list:
        positions_list_clear.append(position)

    return positions_list_clear


def find_players_number(
        columns: list[docx],
        regular_expression: str
) -> list[int]:
    """Функция парсит в искомом столбце номер игрока.
    """
    players_number_list = columns_parser(columns, regular_expression)
    players_number_list_clear = []
    for player_number in players_number_list:
        if len(player_number) > 2:
            players_number_list_clear.append(int(player_number[:2]))
        else:
            players_number_list_clear.append(int(player_number))

    return players_number_list_clear


def find_is_assistants(
        columns: list[docx],
        regular_expression: str
) -> list[bool]:
    """Функция парсит в искомом столбце информацию,
    является ли игрок ассистентом.
    """
    is_assistants_list = columns_parser(columns, regular_expression)
    is_assistants_list_clear = []
    for is_assistant in is_assistants_list:
        if re.search(regular_expression, is_assistant):
            is_assistants_list_clear.append(True)
        else:
            is_assistants_list_clear.append(False)

    return is_assistants_list_clear


def find_is_captain(
        columns: list[docx],
        regular_expression: str
) -> list[bool]:
    """Функция парсит в искомом столбце информацию,
    является ли игрок капитаном.
    """
    is_captain_list = columns_parser(columns, regular_expression)
    is_captain_list_clear = []
    for is_captain in is_captain_list:
        if re.search(regular_expression, is_captain):
            is_captain_list_clear.append(True)
        else:
            is_captain_list_clear.append(False)

    return is_captain_list_clear


def parser() -> list[HockeyData]:
    """Функция собирает все данные об игроке
    и передает их в dataclass.
    """
    hockey_data = []
    columns_from_file = read_file_columns(YANDEX_API, DOWNLOAD_URL)
    text_from_file = read_file_text(YANDEX_API, DOWNLOAD_URL)
    names = find_names(columns_from_file, NAME)
    surnames = find_surnames(columns_from_file, SURNAME)
    dates_of_birth = find_dates_of_birth(
        columns_from_file,
        DATE_OF_BIRTH
    )
    team = find_team(text_from_file, TEAM)
    patronymics = find_patronymics(columns_from_file, PATRONYMIC)
    birth_certificates = find_birth_certificates(
        columns_from_file,
        BIRTH_CERTIFICATE
    )
    passports = find_passports(columns_from_file, PASSPORT)
    positions = find_positions(columns_from_file, POSITION)
    players_number = find_players_number(columns_from_file, PLAYER_NUMBER)
    is_assistants = find_is_assistants(columns_from_file, ASSISTANT)
    is_captain = find_is_captain(columns_from_file, CAPTAIN)

    for index in range(len(names)):
        hockey_data.append(
            HockeyData(
                names[index],
                surnames[index],
                dates_of_birth[index],
                team,
                patronymics[index],
                birth_certificates[index],
                passports[index],
                positions[index],
                players_number[index],
                is_assistants[index],
                is_captain[index]
            )
        )

    return hockey_data


if __name__ == '__main__':
    parser()
