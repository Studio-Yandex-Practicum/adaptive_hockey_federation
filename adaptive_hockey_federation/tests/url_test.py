import pytest
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from fixture_user import (
    test_email,
    test_lastname,
    test_name,
    test_password,
    test_role,
)
from main.models import City, DisciplineName, Team

User = get_user_model()


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

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            password=test_password,
            first_name=test_name,
            last_name=test_lastname,
            role=test_role,
            email=test_email,
        )

        self.team = Team.objects.create(
            name='Test Team',
            city=City.objects.create(name='Test City'),
            discipline_name=DisciplineName.objects.create(
                name='Tetst DisciplineName'),
            curator=self.user
        )
        
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

    def test_main_teams_id_view_returns_200(self):
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
