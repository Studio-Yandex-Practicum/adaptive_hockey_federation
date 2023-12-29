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

    @pytest.mark.django_db(transaction=True)
    def test_urls(self):
        urls = [
            '/users/',
            '/',
            '/players/',
            '/teams/1/',
            '/teams/',
            '/competitions/1/',
            '/competitions/',
            '/analytics/',
            '/unloads/'
        ]
        for url in urls:
            try:
                response = self.client.get(url)
            except Exception as e:
                self.assertEqual(response.status_code, 200),
                f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
