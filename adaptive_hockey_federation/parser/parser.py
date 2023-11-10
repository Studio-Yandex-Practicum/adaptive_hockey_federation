import click

DEFAULT_SOURCE_PATH = 'dsf'


@click.command()
@click.option(
    "--path",
    default=DEFAULT_SOURCE_PATH,
    help="Путь до папки с файлами."
)
@click.option(
    "--print",
    default=False,
    help="Вывод в консоль загруженных данных"
)
def parsing_file(count, name):
    pass


if __name__ == '__main__':
    main()
