from core.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_MODERATOR
from django.core.management.base import BaseCommand
from main.factories.factory import (
    CityFactory,
    DiagnosisFactory,
    NosologyFactory,
    StaffMemberFactory,
    StaffTeamMemberFactory,
)
from users.factories import UserFactory

AMOUNT_ADMIN = 3
AMOUNT_MODERATOR = 2
AMOUNT_AGENT = 15
AMOUTN_COACH = 15
AMOUNT_OTHERS = 10
USERS = {
    ROLE_ADMIN: AMOUNT_ADMIN,
    ROLE_MODERATOR: AMOUNT_MODERATOR,
    ROLE_AGENT: AMOUNT_AGENT
}
STAFF = {
    'Тренер': AMOUTN_COACH,
    'Другие сотрудники': AMOUNT_OTHERS
}

DB_MESSAGE = 'Данные успешно добавлены!'


class Command(BaseCommand):
    help = 'Наполнние базы данных тестовыми данными.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--city',
            action='store_true',
            help='Фикстуры для таблицы City'
        )
        parser.add_argument(
            '-s',
            '--staffmember',
            action='store_true',
            help='Фикстуры для таблицы StaffMember'
        )
        parser.add_argument(
            '-u',
            '--users',
            action='store_true',
            help='Фикстуры для таблицы Users'
        )
        parser.add_argument(
            '-n',
            '--nosology',
            action='store_true',
            help='Фикстуры для таблицы Nosology'
        )
        parser.add_argument(
            '-d',
            '--diagnosis',
            action='store_true',
            help='Фикстуры для таблицы Diagnosis'
        )
        parser.add_argument(
            '-st',
            '--staffteam',
            action='store_true',
            help='Фикстуры для таблицы StaffTeamMember'
        )
        parser.add_argument(
            '-a',
            '--amount',
            type=int,
            default=10,
            help='Количество фикстур для создания')

    def handle(self, *args, **options):
        city = options.get('city', False)
        staff_member = options.get('staffmember', False)
        test_users = options.get('users', False)
        nosology = options.get('nosology', False)
        diagnosis = options.get('diagnosis', False)
        staff_team = options.get('staffteam', False)
        amount = options.get('amount')
        if city:
            CityFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы City создано!'
        if staff_member:
            StaffMemberFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы StaffMemmber создано!'
        if test_users:
            users_amount = sum(USERS.values())
            for role, amount in USERS.items():
                UserFactory.create_batch(amount, role=role)
            return f'{users_amount} фикстур для таблицы User создано!'
        if nosology:
            NosologyFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы Nosology создано!'
        if diagnosis:
            DiagnosisFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы Diagnosis создано!'
        if staff_team:
            staff_amount = sum(STAFF.values())
            for staff_position, amount in STAFF.items():
                StaffTeamMemberFactory.create_batch(
                    amount, staff_position=staff_position
                )
            return (
                f'{staff_amount} фикстур для таблицы StaffTeamMember создано!'
            )
