import json

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from main.models import Diagnosis

from core.config.dev_settings import (
    FILE_MODEL_MAP,
    FIXSTURES_DIR,
)


class Command(BaseCommand):
    """Класс для парсинга данных и их записи в БД."""

    help = "Запуск парсера офисных документов, и запись их в БД."

    def add_arguments(self, parser):
        """Аргументы."""
        parser.add_argument(
            "-f",
            "--fixtures",
            action="store_true",
            help="Фикстуры с реальными данными для таблиц.",
        )

    @transaction.atomic
    def load_real_data(self) -> None:  # noqa: C901
        """Загрузка реальных данных из JSON."""
        with connection.cursor() as cursor:
            for table_name in FILE_MODEL_MAP.keys():
                try:
                    cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
                except Exception as e:
                    return self.stdout.write(
                        self.style.WARNING(
                            f"Не удалось очистить таблицу {table_name}: {str(e)}",  # noqa: E501
                        ),
                    )

        items = list(FILE_MODEL_MAP.items())
        items.reverse()
        for table_name, model_class in items:
            file_path = FIXSTURES_DIR / f"{table_name}.json"
            app_label, model_name = table_name.split("_", 1)
            model = apps.get_model(app_label, model_name)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                for item in data:
                    if table_name == "main_team":
                        team_data = {
                            "id": item["id"],
                            "name": item["name"],
                            "city_id": item["city_id"],
                            "discipline_name_id": item["discipline_name_id"],
                            "curator_id": None,
                        }
                        instance = model(**team_data)
                    elif table_name == "main_player":
                        disciplines = self.get_disciplines()
                        diagnosis = None
                        if item.get("diagnosis_id"):
                            try:
                                diagnosis = Diagnosis.objects.get(
                                    pk=item["diagnosis_id"],
                                )
                            except Diagnosis.DoesNotExist:
                                print(
                                    f"Диагноз с id {item.get('diagnosis_id')} отсутсвует.",  # noqa: E501
                                )
                        player_data = {
                            "id": item["id"],
                            "surname": item["surname"],
                            "name": item["name"],
                            "patronymic": item["patronymic"],
                            "birthday": item["birthday"],
                            "gender": item["gender"],
                            "level_revision": item["level_revision"],
                            "position": item["position"],
                            "number": item["number"],
                            "is_captain": item["is_captain"],
                            "is_assistent": item["is_assistent"],
                            "identity_document": item["identity_document"],
                            "diagnosis": diagnosis,
                            "diagnosis_id": item["diagnosis_id"],
                            "discipline_name_id": disciplines[
                                item["discipline_id"]
                            ]["discipline_name_id"],
                            "discipline_level_id": disciplines[
                                item["discipline_id"]
                            ]["discipline_level_id"],
                        }
                        instance = model(**player_data)
                    else:
                        instance = model(**item)
                    instance.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Данные из {table_name}.json успешно загружены в модель {model_class}",  # noqa: E501
                    ),
                )

            except FileNotFoundError:
                self.stdout.write(
                    self.style.WARNING(f"Файл {table_name}.json не найден"),
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка при загрузке данных из {table_name}.json: {str(e)}",  # noqa: E501
                    ),
                )

    def handle(self, *args, **options):
        """Запись данных в БД."""
        fixtures = options.get("fixtures")
        if fixtures:
            self.load_real_data()

    def get_disciplines(self) -> dict:
        """Получение диспциплин."""
        with open(
            FIXSTURES_DIR / "main_discipline.json",
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)
        disciplines = {
            None: {"discipline_level_id": None, "discipline_name_id": None},
        }
        for item in data:
            disciplines[item["id"]] = {
                "discipline_level_id": item["discipline_level_id"],
                "discipline_name_id": item["discipline_name_id"],
            }
        return disciplines
