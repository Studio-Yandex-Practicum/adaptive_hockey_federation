import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from fixture_user import (
    test_email,
    test_lastname,
    test_name,
    test_password,
    test_role,
)

User = get_user_model()


class TestAuthUrls:

    @pytest.mark.django_db(transaction=True)
    def test_auth_urls(self, client):
        urls = ['/auth/login/', '/auth/logout/']
        for url in urls:
            try:
                response = client.get(url)
            except Exception as e:
                assert False, (
                    f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
                )
            assert response.status_code != 404, (
                f'''Страница `{url}` не найдена,
                проверьте этот адрес в *urls.py*'''
            )
            assert response.status_code == 200, (
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

    def test_users_list_view_returns_200(self):
        self.client.force_login(self.user)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

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
