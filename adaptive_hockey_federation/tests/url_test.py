from copy import copy
from collections import namedtuple
from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from tests.fixture_user import (
    test_email,
    test_lastname,
    test_name,
    test_password,
    test_role,
)
from main.data_factories.factories import EventFactory, PlayerFactory, \
    DiagnosisFactory
from main.models import (
    City,
    DisciplineName,
    StaffMember,
    StaffTeamMember,
    Team,
)

User = get_user_model()


class UrlToTest:
    """Класс для использования в автоматизации тестирования урлов."""

    def __init__(
            self,
            path: str,
            code_estimated: int = HTTPStatus.OK,
            permission_required: str = None,
            authorized_only: bool = True,
            unauthorized_code_estimated: int = HTTPStatus.FOUND
    ):
        self.path = path
        self.authorized_only = authorized_only
        self.code_estimated = code_estimated
        if permission_required:
            self.permission = Permission.objects.get(
                codename=permission_required
            )
        else:
            self.permission = None
        if self.authorized_only:
            self.unauthorized_code = unauthorized_code_estimated
        else:
            self.unauthorized_code = HTTPStatus.OK

    def unauthorized_test(self, client: Client):
        """Возвращает "ответ-ожидание" для неавторизованного пользователя."""
        client.logout()
        response = client.get(self.path)
        message = (f'Для неавторизованного пользователя страница {self.path} '
                   f'должна вернуть ответ со статусом '
                   f'{self.unauthorized_code}.')
        return response.status_code, self.unauthorized_code, message

    def permissioned_test(self, client: Client, user: User):
        user.user_permissions.add(self.permission)
        client.force_login(user)
        response = client.get(self.path)
        message = (f'Для пользователя, обладающего разрешением '
                   f'{self.permission.codename} страница {self.path} '
                   f'должна вернуть ответ со статусом '
                   f'{self.code_estimated}.')
        return response.status_code, self.code_estimated, message

    def unpermissioned_test(self, client: Client, user: User):
        user.user_permissions.clear()
        client.force_login(user)
        response = client.get(self.path)
        message = (f'Для пользователя, не обладающего разрешением '
                   f'{self.permission.codename} страница {self.path} '
                   f'должна вернуть ответ со статусом '
                   f'{HTTPStatus.FORBIDDEN}.')
        return response.status_code, HTTPStatus.FORBIDDEN, message

    def authorized_test(self, client: Client, user: User):
        """Возвращает "ответ-ожидание" для авторизованного пользователя."""
        user.user_permissions.clear()
        client.force_login(user)
        response = client.get(self.path)
        message = (f'Для любого авторизованного пользователя, страница '
                   f'{self.path} должна вернуть ответ со статусом '
                   f'{self.code_estimated}.')
        return response.status_code, self.code_estimated, message

    def get_equals(self, client: Client, user: User):
        res = [self.unauthorized_test(client)]
        if self.permission:
            res.append(self.permissioned_test(client, user))
            res.append(self.unpermissioned_test(client, user))
        else:
            res.append(self.authorized_test(client, user))

        return res


class TestAuthUrls:

    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        urls = {'/auth/login/': 200, '/auth/logout/': 302}
        for url, status in urls.items():
            try:
                response = client.post(url)
            except Exception as e:
                assert False, (
                    f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
                )
            assert response.status_code != 404, (
                f'''Страница `{url}` не найдена,
                проверьте этот адрес в *urls.py*'''
            )
            assert response.status_code == status, (
                f'''Ошибка {response.status_code} при открытиии `{url}`.
                Проверьте ее view-функцию'''
            )


class TestUrls(TestCase):
    user: User
    team: Team

    @classmethod
    def setUpClass(cls) -> None:
        """Создает необходимые сущности (объекты моделей БД).
        Запускается только один раз (в отличие от метода setUp),
        не сбрасывается после каждого теста, что помогает
        избежать многократного создания сущностей и, как следствие, смены id
        каждой сущности после каждого теста."""
        super().setUpClass()
        cls.user = User.objects.create_user(
            password=test_password,
            first_name="cls_" + test_name,
            last_name="cls_" + test_lastname,
            role=test_role,
            email="cls_" + test_email,
        )

        cls.team = Team.objects.create(
            name='cls_Test Team',
            city=City.objects.create(name='cls_Test City'),
            discipline_name=DisciplineName.objects.create(
                name='cls_Test DisciplineName'),
            curator=cls.user,
        )
        cls.competition = EventFactory.create()
        cls.diagnosis = DiagnosisFactory.create()
        cls.player = PlayerFactory.create()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            password=test_password,
            first_name=test_name,
            last_name=test_lastname,
            role=test_role,
            email=test_email,
        )
        self.permissions = {
            'view_team': Permission.objects.get(codename='view_team')
        }

        self.staff_member = StaffMember.objects.create(
            name='Test Name', surname='Test Surname')
        self.staff_team_member = StaffTeamMember.objects.create(
            staff_member=self.staff_member, staff_position='Test Staff')
        self.team = Team.objects.create(
            name='Test Team 2',
            city=City.objects.create(name='Test City 2'),
            discipline_name=DisciplineName.objects.create(
                name='Tetst DisciplineName 2'),
            curator=self.user,
        )
        self.competition = EventFactory.create()

    def delete_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False

    def test_create_user(self):
        # Тест - создание пользователя
        self.assertEqual(self.user.first_name, test_name)
        self.assertEqual(self.user.last_name, test_lastname)
        self.assertEqual(self.user.role, test_role)
        self.assertEqual(self.user.email, test_email)

    def test_edit_user(self):
        # Тест - редактирование существующего пользователя
        new_name = 'Test'
        new_lastname = 'User'
        new_role = 'Tester'
        new_email = 'test@example.com'

        self.user.first_name = new_name
        self.user.last_name = new_lastname
        self.user.role = new_role
        self.user.email = new_email
        self.user.save()

        edited_user = User.objects.get(email=new_email)
        self.assertEqual(edited_user.first_name, new_name)
        self.assertEqual(edited_user.last_name, new_lastname)
        self.assertEqual(edited_user.role, new_role)
        self.assertEqual(edited_user.email, new_email)

    def test_delete_user(self):
        # Тест - удаление пользователя
        delete_result = self.delete_user(self.user.id)
        self.assertTrue(delete_result, 'Ошибка при удалении пользователя')

    def test_users_list_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_user_update_view_returns_200(self):
        self.adminuser = User.objects.get(first_name='admin')

        self.permission = Permission.objects.get(codename='change_user')
        self.adminuser.user_permissions.add(self.permission)
        self.adminuser.save()

        self.client.force_login(self.adminuser)

        response = self.client.get('/user_update/1/')
        assert response.status_code == 200

    def test_main_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_players_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/players/')
        self.assertEqual(response.status_code, 200)

    # TODO Раскомментировать и изменить при работе с тестами на пермишены
    def test_main_teams_id_view_returns_200(self):

        self.user.user_permissions.add(self.permissions['view_team'])
        print(self.user.user_permissions.all())
        print(self.team.id)
        self.client.force_login(self.user)
        response = self.client.get('/teams/1/')
        self.assertEqual(response.status_code, 200)

    def test_main_teams_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, 200)

    def test_main_competitions_id_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/competitions/1/')
        self.assertEqual(response.status_code, 200)

    def test_main_competitions_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/competitions/')
        self.assertEqual(response.status_code, 200)

    def test_main_analytics_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/analytics/')
        self.assertEqual(response.status_code, 200)

    def test_main_unloads_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/unloads/')
        self.assertEqual(response.status_code, 200)

    def test_main_urls(self):
        urls = [
            UrlToTest('/', HTTPStatus.OK, None),
            UrlToTest('/analytics/', HTTPStatus.OK, None),
            UrlToTest('/competitions/', HTTPStatus.OK, None),
            UrlToTest('/competitions/1/', HTTPStatus.OK, None),
            UrlToTest('/player_create/', HTTPStatus.OK, None),
            UrlToTest('/players/', HTTPStatus.OK, None),
            UrlToTest('/players/1/', HTTPStatus.OK, None),
            UrlToTest('/players/1/edit/', HTTPStatus.OK, None),
            UrlToTest('/teams/', HTTPStatus.OK, None),
            UrlToTest('/teams/1/', HTTPStatus.OK, 'view_team'),
            UrlToTest('/teams/1/edit/', HTTPStatus.OK, 'change_team'),
            UrlToTest('/teams/create/', HTTPStatus.OK, 'add_team'),
            UrlToTest('/unloads/', HTTPStatus.OK, None),
            UrlToTest('/user_create/', HTTPStatus.OK, 'add_user'),
            UrlToTest('/user_update/1/', HTTPStatus.OK, 'change_user'),
        ]
        urls_responses_results = []

        for url in urls:
            urls_responses_results += url.get_equals(self.client, self.user)

        for fact, estimated, message in urls_responses_results:
            with self.subTest(msg=message, fact=fact, estimated=estimated):
                self.assertEqual(fact, estimated, message)
