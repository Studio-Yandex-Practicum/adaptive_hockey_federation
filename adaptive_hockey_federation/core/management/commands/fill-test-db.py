from random import randint

from core.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_MODERATOR
from django.core.management.base import BaseCommand
from main.data_factories.factories import (
    DiagnosisFactory,
    DisciplineFactory,
    DocumentFactory,
    PlayerFactory,
    StaffTeamMemberFactory,
    TeamFactory,
)
from main.data_factories.utils import updates_for_players
from main.models import Player
from users.factories import UserFactory

AMOUNT_ADMIN = 3
AMOUNT_MODERATOR = 2
AMOUNT_AGENT = 15
AMOUNT_COACH = 15
AMOUNT_OTHERS = 10
USERS = {
    ROLE_ADMIN: AMOUNT_ADMIN,
    ROLE_MODERATOR: AMOUNT_MODERATOR,
    ROLE_AGENT: AMOUNT_AGENT,
}
STAFF = {"Тренер": AMOUNT_COACH, "Другие сотрудники": AMOUNT_OTHERS}


class Command(BaseCommand):
    help = "Наполнение базы данных тестовыми данными."

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--users", action="store_true",
            help="Фикстуры для таблицы Users",
        )
        parser.add_argument(
            "-d",
            "--diagnosis",
            action="store_true",
            help="Фикстуры для таблицы Diagnosis",
        )
        parser.add_argument(
            "-s",
            "--staffteam",
            action="store_true",
            help="Фикстуры для таблицы StaffTeamMember",
        )
        parser.add_argument(
            "-ds",
            "--discipline",
            action="store_true",
            help="Фикстуры для таблицы Discipline",
        )
        parser.add_argument(
            "-t", "--team", action="store_true",
            help="Фикстуры для таблицы Team",
        )
        parser.add_argument(
            "-p", "--player", action="store_true",
            help="Фикстуры для таблицы Player",
        )
        parser.add_argument(
            "-doc", "--document", action="store_true",
            help="Фикстуры для таблицы Document",
        )
        parser.add_argument(
            "-a",
            "--amount",
            type=int,
            default=10,
            help="Количество фикстур для создания",
        )

    def handle(self, *args, **options):  # noqa: C901
        test_users = options.get("users", False)
        diagnosis = options.get("diagnosis", False)
        staff_team = options.get("staffteam", False)
        discipline = options.get("discipline", False)
        team = options.get("team", False)
        player = options.get("player", False)
        document = options.get("document", False)
        amount = options.get("amount")
        if test_users:
            users_amount = sum(USERS.values())
            for role, amount in USERS.items():
                UserFactory.create_batch(amount, role=role)
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{users_amount} фикстур для таблицы User создано!"
                )
            )
        if diagnosis:
            DiagnosisFactory.create_batch(amount)
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{amount} фикстур для таблицы Diagnosis создано!"
                )
            )
        if staff_team:
            staff_amount = sum(STAFF.values())
            for staff_position, amount in STAFF.items():
                StaffTeamMemberFactory.create_batch(
                    amount, staff_position=staff_position
                )
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{staff_amount} фикстур для таблицы "
                    "StaffTeamMember создано!"
                )
            )
        if discipline:
            DisciplineFactory.create_batch(amount)
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{amount} фикстур для таблицы Discipline созданы!"
                )
            )

        if team:
            TeamFactory.create_batch(amount)
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{amount} фикстур для таблицы Team созданы!"
                )
            )
        if player:
            PlayerFactory.create_batch(amount)
            updates_for_players()
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{amount} фикстур для таблицы Player созданы!"
                )
            )
        if document:
            players = Player.objects.all()
            for player in players:
                num_docs = randint(1, 5)
                DocumentFactory.create_batch(num_docs, player=player)
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{num_docs} фикстур для таблицы Document созданы!"
                )
            )
