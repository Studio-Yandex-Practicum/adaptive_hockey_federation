from datetime import datetime
from typing import Any

from django.test import TestCase
from main.data_factories.factories import (
    DiagnosisFactory,
    DisciplineFactory,
    PlayerFactory,
)
from main.models import Diagnosis, Discipline, Player


class TestUser(TestCase):
    """Тестирование CRUD игрока
    с использованием фабрик."""

    diagnosis: Diagnosis | Any = None
    player: Player | Any = None
    player_test: Player | Any = None
    discipline: Discipline | Any = None

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        cls.diagnosis = DiagnosisFactory.create()
        cls.discipline = DisciplineFactory.create()
        cls.player = PlayerFactory.create()
        cls.player_test = cls.player

    def setUp(self):

        self.player = Player.objects.create(
            surname=self.player_test.surname + "тест",
            name=self.player_test.name + "тест",
            patronymic=self.player_test.patronymic + "тест",
            gender=self.player_test.gender,
            birthday=self.player_test.birthday,
            discipline=self.discipline,
            diagnosis=self.diagnosis,
            level_revision=self.player_test.level_revision,
            position=self.player_test.position,
            number=self.player_test.number,
            identity_document=self.player_test.identity_document,
        )
        self.discipline = self.player.discipline
        self.diagnosis = self.player.diagnosis

    # TODO: Добавить проверку пермишенов
    def test_player_create(self):
        """Тест - создание игрока."""
        self.assertEqual(
            self.player.surname, self.player_test.surname + "тест"
        )
        self.assertEqual(self.player.name, self.player_test.name + "тест")
        self.assertEqual(
            self.player.patronymic, self.player_test.patronymic + "тест"
        )
        self.assertEqual(self.player.gender, self.player_test.gender)
        self.assertEqual(self.player.birthday, self.player_test.birthday)
        self.assertEqual(self.player.discipline, self.discipline)
        self.assertEqual(self.player.diagnosis, self.diagnosis)
        self.assertEqual(
            self.player.level_revision, self.player_test.level_revision
        )
        self.assertEqual(self.player.position, self.player_test.position)
        self.assertEqual(self.player.number, self.player_test.number)
        self.assertEqual(
            self.player.identity_document, self.player_test.identity_document
        )

    # TODO: Добавить проверку пермишенов
    def test_player_edit(self):
        """Тест - редактирование существующего игрока."""
        new_surname = self.player_test.surname + "редактирование"
        new_name = self.player_test.name + "редактирование"
        new_patronymic = self.player_test.patronymic + "редактирование"
        new_gender = self.player_test.gender
        new_birthday = datetime.strptime("2014-01-18", "%Y-%m-%d").date()
        new_discipline = DisciplineFactory.create()
        new_diagnosis = DiagnosisFactory.create()
        new_level_revision = self.player_test.level_revision + "ред."
        new_position = self.player_test.position + "редактирование"
        new_number = self.player_test.number + 1
        new_identity_document = self.player_test.identity_document + "ред."

        self.player.surname = new_surname
        self.player.name = new_name
        self.player.patronymic = new_patronymic
        self.player.gender = new_gender
        self.player.birthday = new_birthday
        self.player.discipline = new_discipline
        self.player.diagnosis = new_diagnosis
        self.player.level_revision = new_level_revision
        self.player.position = new_position
        self.player.number = new_number
        self.player.identity_document = new_identity_document
        self.player.save()

        edited_player = Player.objects.get(pk=self.player.pk)
        self.assertEqual(edited_player.surname, new_surname)
        self.assertEqual(edited_player.name, new_name)
        self.assertEqual(edited_player.patronymic, new_patronymic)
        self.assertEqual(edited_player.gender, new_gender)
        self.assertEqual(edited_player.birthday, new_birthday)
        self.assertEqual(edited_player.discipline, new_discipline)
        self.assertEqual(edited_player.diagnosis, new_diagnosis)
        self.assertEqual(edited_player.level_revision, new_level_revision)
        self.assertEqual(edited_player.position, new_position)
        self.assertEqual(edited_player.number, new_number)
        self.assertEqual(
            edited_player.identity_document, new_identity_document
        )

    def delete_player(self, player_id):
        try:
            player = Player.objects.get(id=player_id)
            player.delete()
            return True
        except Player.DoesNotExist:
            return False

    # TODO: Добавить проверку пермишенов
    def test_player_delete(self):
        """Тест - удаление игрока."""
        delete_result = self.delete_player(self.player.id)
        self.assertTrue(delete_result, "Ошибка при удалении игрока")
