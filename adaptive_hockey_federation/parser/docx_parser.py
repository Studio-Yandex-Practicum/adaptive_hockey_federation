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
PASSPORT = '[П|п][А|а][С|с][П|п][О|о][Р|р][Т|т]'
POSITION = '[П|п][О|о][З|з][И|и][Ц|ц][И|и][Я|я]'
PLAYER_NUMBER = '[И|и][Г|г].+[Н|н][О|о][М|м][Е|е][Р|р]'
ASSISTANT = '[А|а][С|с][С|с][И|и][С|с][Т|т][Е|е][Н|н][Т|т]'
CAPTAIN = '[К|к][А|а][П|п][И|и][Т|т][А|а][Н|н]'

YANDEX_API = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
DOWNLOAD_URL = 'https://disk.yandex.ru/i/ZRusBovQDTl5zw'


def load_file(ya_api: str, download_url: str) -> docx:
    """Функция загружает данные из файла по ссылке.
    """
    response = requests.get(
        ya_api + urlencode(dict(public_key=download_url)),
    )
    download_response = requests.get(response.json()['href'])
    with tempfile.TemporaryFile() as file:
        file.write(download_response.content)
        return docx.Document(file)


def read_file_columns(file: docx) -> list[docx]:
    """Функция находит таблицы в файле и возвращает список объектов
    docx с данными каждого столбца.
    """
    return [
        column
        for table in file.tables
        for index, column in enumerate(table.columns)
    ]


def read_file_text(file: docx) -> list[docx]:
    """Функция находит текстовые данные в файле и возвращает список объектов
    docx с найденными данными.
    """
    return [
        run.text
        for paragraph in file.paragraphs
        for run in paragraph.runs
    ]


def columns_parser(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция находит столбец по названию и списком выводит содержимое
    каждой ячейки этого столбца.
    """
    return [
        text
        if text
        else None
        for column in columns
        if re.search(
            regular_expression,
            list(cell.text for cell in column.cells)[0]
        )
        for text in list(cell.text for cell in column.cells)[1:]

    ]


def find_names(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце имена. Если имя записано
    вместе с фамилией и отчеством, то функция опирается на шаблон ФИО
    (имя идет после фамилии на втором месте).
    """
    names_list = columns_parser(columns, regular_expression)
    return [
        name.split()[1]
        if len(name.split()) > 1
        else name
        for name in names_list
    ]


def find_surnames(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце фамилии. Если фамилия записана
    вместе с именем и отчеством, то функция опирается на шаблон ФИО
    (фамилия идет на первом месте).
    """
    surnames_list = columns_parser(columns, regular_expression)
    return [
        surname.split()[0]
        if len(surname.split()) > 1
        else surname
        for surname in surnames_list
    ]


def find_dates_of_birth(
        columns: list[docx],
        regular_expression: str,
) -> list[date]:
    """Функция парсит в искомом столбце дату рождения
    и опирается на шаблон дд.мм.гггг.
    """
    dates_of_birth_list = columns_parser(columns, regular_expression)
    return [
        date(int(year), int(month), int(day))
        for date_of_birth in dates_of_birth_list
        for day, month, year in [date_of_birth.split('.')]
    ]


def find_team(text: list[str], regular_expression: str) -> str:
    """Функция парсит название команды.
    """
    return [
        text[index + 2]
        for index, txt in enumerate(text)
        if re.search(regular_expression, txt)
    ][0]


def find_patronymics(
        columns: list[docx],
        regular_expression: str,
) -> list[str]:
    """Функция парсит в искомом столбце отчества. Если отчество записано
    вместе с именем и фамилией, то функция опирается на шаблон ФИО
    (отчество идет на последнем месте).
    """
    patronymics_list = columns_parser(columns, regular_expression)
    return [
        patronymic.split()[2]
        if len(patronymic.split()) > 1
        else patronymic
        for patronymic in patronymics_list
    ]


def find_birth_certificates(
        columns: list[docx],
        regular_expression: str,
) -> list[str]:
    """Функция парсит в искомом столбце данные свидетельства о рождении.
    """
    birth_certificates_list = columns_parser(columns, regular_expression)
    return [
        re.sub(regular_expression, '', birth_certificate).replace('\n', ' ')
        if re.search(regular_expression, birth_certificate)
        else None
        for birth_certificate in birth_certificates_list
    ]


def find_passports(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце данные паспорта.
    """
    passports_list = columns_parser(columns, regular_expression)
    return [
        re.sub(regular_expression, '', passport).replace('\n', ' ')
        if re.search(regular_expression, passport)
        else None
        for passport in passports_list
    ]


def find_positions(columns: list[docx], regular_expression: str) -> list[str]:
    """Функция парсит в искомом столбце позицию игрока на поле.
    """
    positions_list = columns_parser(columns, regular_expression)
    return [
        position
        for position in positions_list
    ]


def find_players_number(
        columns: list[docx],
        regular_expression: str,
) -> list[int]:
    """Функция парсит в искомом столбце номер игрока.
    """
    players_number_list = columns_parser(columns, regular_expression)
    return [
        int(player_number[:2])
        if len(player_number) > 2
        else int(player_number)
        for player_number in players_number_list
    ]


def find_is_assistants(
        columns: list[docx],
        regular_expression: str,
) -> list[bool]:
    """Функция парсит в искомом столбце информацию,
    является ли игрок ассистентом.
    """
    is_assistants_list = columns_parser(columns, regular_expression)
    return [
        True
        if re.search(regular_expression, is_assistant)
        else False
        for is_assistant in is_assistants_list
    ]


def find_is_captain(
        columns: list[docx],
        regular_expression: str,
) -> list[bool]:
    """Функция парсит в искомом столбце информацию,
    является ли игрок капитаном.
    """
    is_captain_list = columns_parser(columns, regular_expression)
    return [
        True
        if re.search(regular_expression, is_captain)
        else False
        for is_captain in is_captain_list
    ]


def parser(file: docx) -> list[HockeyData]:
    """Функция собирает все данные об игроке
    и передает их в dataclass.
    """
    columns_from_file = read_file_columns(file)
    text_from_file = read_file_text(file)
    names = find_names(columns_from_file, NAME)
    surnames = find_surnames(columns_from_file, SURNAME)
    dates_of_birth = find_dates_of_birth(
        columns_from_file,
        DATE_OF_BIRTH,
    )
    team = find_team(text_from_file, TEAM)
    patronymics = find_patronymics(columns_from_file, PATRONYMIC)
    birth_certificates = find_birth_certificates(
        columns_from_file,
        BIRTH_CERTIFICATE,
    )
    passports = find_passports(columns_from_file, PASSPORT)
    positions = find_positions(columns_from_file, POSITION)
    players_number = find_players_number(columns_from_file, PLAYER_NUMBER)
    is_assistants = find_is_assistants(columns_from_file, ASSISTANT)
    is_captain = find_is_captain(columns_from_file, CAPTAIN)

    return [
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
            is_captain[index],
        )
        for index in range(len(names))
    ]


if __name__ == '__main__':
    docx_file = load_file(YANDEX_API, DOWNLOAD_URL)
    parser(docx_file)
