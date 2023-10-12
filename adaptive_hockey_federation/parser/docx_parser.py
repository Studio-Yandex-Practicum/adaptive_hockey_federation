import re
from collections import defaultdict as dd
from datetime import date
from urllib.parse import urlencode

import docx
import requests
from adaptive_hockey_federation.core.user_card import HockeyData

NAME = '[И|и][М|м][Я|я]'
SURNAME = '[Ф|ф][А|а][М|м][И|и][Л|л][И|и][Я|я]'
DATE_OF_BIRTH = '[Д|д][А|а][Т|т][А|а]'
BIRTH_CERTIFICATE = '[С|с][В|в].+?[В|в][О|о]'
PASSPORT = '[П|п][А|а][С|с][П|п][О|о][Р|р][Т|т]'
POSITION = '[П|п][О|о][З|з][И|и][Ц|ц][И|и][Я|я]'
PLAYER_NUMBER = '[И|и][Г|г].+[Н|н][О|о][М|м][Е|е][Р|р]'
ASSISTANT = '[А|а][С|с][С|с][И|и][С|с][Т|т][Е|е][Н|н][Т|т]'
CAPTAIN = '[К|к][А|а][П|п][И|и][Т|т][А|а][Н|н]'


main_data = dd(list)


def read_file() -> docx:
    """Функция загружает файл по ссылке в рабочий каталог,
    находит таблицы в документе и возвращает объект
    docx с данными каждого столбца.
    """
    base_url = (
        'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    )
    public_key = 'https://disk.yandex.ru/i/ZRusBovQDTl5zw'
    work_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(work_url)
    download_url = response.json()['href']
    download_response = requests.get(download_url)
    with open('work_file.docx', 'wb') as file:
        file.write(download_response.content)
    document = docx.Document('work_file.docx')
    all_columns = []
    for table in document.tables:
        for index, column in enumerate(table.columns):
            all_columns.append(column)

    return all_columns


def columns_parser(columns: list[docx], column_name: str) -> list[str]:
    """Функция находит столбец по названию и списком выводит содержимое
    каждой ячейки этого столбца.
    """
    column_data = []
    for column in columns:
        cell_text = list(cell.text for cell in column.cells)
        if re.search(column_name, cell_text[0]):
            for text in cell_text[1:]:
                column_data.append(text)

    return column_data


def find_user_names(columns: list[docx], user_name: str) -> None:
    """Функция парсит в искомом столбце имена. Если имя записано
    вместе с фамилией и отчеством, то функция опирается на шаблон ФИО
    (имя идет после фамилии на втором месте).
    """
    names_list = columns_parser(columns, user_name)
    index = 0
    for name in names_list:
        index += 1
        if len((str(name).split())) > 1:
            main_data[index].append(str(name).split()[1])
        else:
            main_data[index].append(name)


def find_user_surnames(columns: list[docx], user_surname: str) -> None:
    """Функция парсит в искомом столбце фамилии. Если фамилия записана
    вместе с именем и отчеством, то функция опирается на шаблон ФИО
    (фамилия идет на первом месте).
    """
    surnames_list = columns_parser(columns, user_surname)
    index = 0
    for surname in surnames_list:
        index += 1
        if len((str(surname).split())) > 1:
            main_data[index].append(str(surname).split()[0])
        else:
            main_data[index].append(surname)


def find_user_dates_of_birth(columns: list[docx], date_of_birth: str) -> None:
    """Функция парсит в искомом столбце дату рождения
    и опирается на шаблон дд.мм.гггг.
    """
    dates_list = columns_parser(columns, date_of_birth)
    index = 0
    for user_date in dates_list:
        index += 1
        day, month, year = str(user_date).split('.')
        main_data[index].append(date(int(year), int(month), int(day)))


def find_birth_certificate(columns: list[docx], passport: str) -> None:
    """Функция парсит в искомом столбце данные свидетельства о рождении.
    """
    birth_certificates_list = columns_parser(columns, passport)
    index = 0
    for user_birth_certificate in birth_certificates_list:
        index += 1
        if re.search(BIRTH_CERTIFICATE, user_birth_certificate):
            text = re.sub(BIRTH_CERTIFICATE, '', user_birth_certificate)
            main_data[index].append(str(text).replace('\n', ''))
        else:
            main_data[index].append(None)


def find_passports(columns: list[docx], passport: str) -> None:
    """Функция парсит в искомом столбце данные паспорта.
    """
    passports_list = columns_parser(columns, passport)
    index = 0
    for user_passport in passports_list:
        index += 1
        if re.search(PASSPORT, user_passport):
            text = re.sub(PASSPORT, '', user_passport)
            main_data[index].append(str(text).replace('\n', ''))
        else:
            main_data[index].append(None)


def find_positions(columns: list[docx], position: str) -> None:
    """Функция парсит в искомом столбце позицию игрока на поле.
    """
    positions_list = columns_parser(columns, position)
    index = 0
    for user_position in positions_list:
        index += 1
        main_data[index].append(user_position)


def find_players_number(columns: list[docx], player_number: str) -> None:
    """Функция парсит в искомом столбце номер игрока.
    """
    players_number_list = columns_parser(columns, player_number)
    index = 0
    for number in players_number_list:
        index += 1
        if len(number) > 2:
            main_data[index].append(int(number[:2]))
        else:
            main_data[index].append(int(number))


def find_is_assistants(columns: list[docx], is_assistant: str) -> None:
    """Функция парсит в искомом столбце информацию,
    является ли игрок ассистентом.
    """
    is_assistants_list = columns_parser(columns, is_assistant)
    index = 0
    for assistant in is_assistants_list:
        index += 1
        if re.search(ASSISTANT, assistant):
            main_data[index].append(True)
        else:
            main_data[index].append(False)


def find_is_captain(columns: list[docx], is_captain: str) -> None:
    """Функция парсит в искомом столбце информацию,
    является ли игрок капитаном.
    """
    is_captain_list = columns_parser(columns, is_captain)
    index = 0
    for captain in is_captain_list:
        index += 1
        if re.search(CAPTAIN, captain):
            main_data[index].append(True)
        else:
            main_data[index].append(False)


if __name__ == '__main__':
    columns_from_file = read_file()
    find_user_names(columns_from_file, NAME)
    find_user_surnames(columns_from_file, SURNAME)
    find_user_dates_of_birth(
        columns_from_file,
        DATE_OF_BIRTH
    )
    find_birth_certificate(
        columns_from_file,
        PASSPORT
    )
    find_passports(columns_from_file, PASSPORT)
    find_positions(columns_from_file, POSITION)
    find_players_number(columns_from_file, PLAYER_NUMBER)
    find_is_assistants(columns_from_file, ASSISTANT)
    find_is_captain(columns_from_file, CAPTAIN)

    for key, value in main_data.items():
        (
            name,
            surname,
            birth_of_date,
            birth_certificate,
            passport, position,
            player_number,
            assistant,
            captain
        ) = value
        FromDocxAdditionalUserInfo(
            name,
            surname,
            birth_of_date,
            birth_certificate,
            passport,
            position,
            player_number,
            assistant,
            captain
        )
