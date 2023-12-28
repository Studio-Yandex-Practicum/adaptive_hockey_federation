from core.constants import ROLE_ADMIN, ROLE_AGENT, ROLE_MODERATOR
from django.core.management.base import BaseCommand
from main.factories import CityFactory, StaffMemberFactory
from users.factories import UserFactory

ROLES = [ROLE_AGENT, ROLE_MODERATOR, ROLE_ADMIN]
TEST_USERS_AMOUNT = 3
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
            '-a',
            '--amount',
            type=int,
            default=10,
            help='Количество фикстур для создания')

    def handle(self, *args, **options):
        city = options.get('city', False)
        staff_member = options.get('staffmember', False)
        test_users = options.get('users', False)
        amount = options.get('amount')
        if city:
            CityFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы City создано!'
        if staff_member:
            StaffMemberFactory.create_batch(amount)
            return f'{amount} фикстур для таблицы StaffMemmber создано!'
        if test_users:
            for role in ROLES:
                UserFactory.create_batch(amount, role=role)
        self.stdout.write(self.style.SUCCESS(DB_MESSAGE))
