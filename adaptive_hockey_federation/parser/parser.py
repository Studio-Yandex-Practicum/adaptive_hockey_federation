import json
import os
from pprint import pprint

import click
import docx  # type: ignore

from adaptive_hockey_federation.core.config.dev_settings import (
    FIXSTURES_DIR, FIXSTURES_FILE)
from adaptive_hockey_federation.parser.docx_parser import (
    docx_parser, find_numeric_statuses)
from adaptive_hockey_federation.parser.xlsx_parser import xlsx_parser

NUMERIC_STATUSES = "Числовые статусы следж-хоккей 02.10.203.docx"
FILES_BLACK_LIST = [
    "На мандатную комиссию",
    "Именная заявка следж-хоккей Энергия Жизни Сочи",
    "ФАХ Сияжар Взрослые",
    "Числовые статусы следж-хоккей 02.10.203",
]
FILES_EXTENSIONS = [
    ".docx",
    ".xlsx",
]
NUMERIC_STATUSES_FILE_ERROR = (
    "Не могу найти {}. Без него не"
    " получиться загрузить именные заявки."
    " Файл должен находиться в директории с"
    " файлами для парсинга"
)


@click.command()
@click.option(
    "-p",
    "--path",
    required=True,
    help="Путь до папки с файлами для парсинга",
)
@click.option(
    "-r",
    "--result",
    is_flag=True,
    help="Вывод в консоль извлеченных данных и статистики",
)
def parsing_file(path: str, result: bool) -> None:
    """Функция запускает парсинг файлов в рамках проекта.
    Запуск через командную строку:
    'python parser.py -p(--path) путь_до_папки_с_файлами'
    Вызов справки 'python parser.py -h(--help)'
    """
    results_list = []
    files, numeric_statuses_file = get_all_files(path)
    if numeric_statuses_file is None:
        click.echo(NUMERIC_STATUSES_FILE_ERROR.format(NUMERIC_STATUSES))
        return
    numeric_statuses = find_numeric_statuses(docx.Document(numeric_statuses_file))
    click.echo(f"Найдено {len(files)} файлов.")
    for file in files:
        if file.endswith("docx"):
            results_list.extend(docx_parser(file, numeric_statuses))
        else:
            results_list.extend(xlsx_parser(file))  # type: ignore
    if result:
        for data in results_list:
            pprint(data)

    if not os.path.exists(FIXSTURES_DIR):
        os.makedirs(FIXSTURES_DIR)
    json.dump(
        results_list,
        open(FIXSTURES_FILE, "w", encoding="utf8"),
        ensure_ascii=False,
        indent=4,
        default=str,
    )

    results_list = list(results_list)

    click.echo(f"Успешно обработано {len(files)} файлов.")
    click.echo(f"Извлечено {len(results_list)} уникальных записей")


def get_all_files(path: str) -> tuple[list[str], str | None]:
    """Функция извлекает из папки, в том числе вложенных,
    список всех файлов и отдельно путь до файла с числовыми статусами.
    Извлекаются только файлы с расширениями указанными в константе
    FILES_EXTENSIONS (по умолчанию docx, xlsx) и не извлекает файлы, название
    которых без расширения указано в списке FILES_BLACK_LIST.
    """
    files = []
    numeric_statuses_filepath = None
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename == NUMERIC_STATUSES:
                numeric_statuses_filepath = os.path.join(dirpath, filename)
            file, extension = os.path.splitext(filename)
            if (
                not file.startswith("~")
                and extension in FILES_EXTENSIONS
                and file not in FILES_BLACK_LIST
            ):
                files.append(os.path.join(dirpath, filename))
    return files, numeric_statuses_filepath


if __name__ == "__main__":
    parsing_file()
