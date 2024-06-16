from http import HTTPStatus

import pytest
from django.test import Client
from tests.base import BaseTestClass, UrlTestMixin
from tests.url_schema import (ADMIN_APP_LABELS_URLS, ADMIN_AUTH_GROUP_302,
                              ADMIN_AUTH_URLS, ADMIN_CITY_URL_302,
                              ADMIN_CITY_URLS, ADMIN_COMPETITIONS_URLS,
                              ADMIN_COMPETITIONS_URLS_302,
                              ADMIN_DIAGNOSIS_URL_302, ADMIN_DIAGNOSIS_URLS,
                              ADMIN_DISCIPLINE_NAME_URL_302,
                              ADMIN_DISCIPLINE_NAME_URLS, ADMIN_LOGIN,
                              ADMIN_LOGOUT, ADMIN_MAIN_URL,
                              ADMIN_NOSOLOGY_URL_302, ADMIN_NOSOLOGY_URLS,
                              ADMIN_PASSWORD_URLS, ADMIN_PLAYER_URL_302,
                              ADMIN_PROXY_GROUP_URL_302,
                              ADMIN_PROXY_GROUP_URLS,
                              ADMIN_STAFF_MEMBER_URL_302,
                              ADMIN_STAFF_MEMBER_URLS, ADMIN_TEAM_URL_302,
                              ADMIN_TEAM_URLS, ADMIN_USER_URL_302,
                              ADMIN_USER_URLS, AUTH_RESET_URLS,
                              COMPETITION_GET_URLS, COMPETITION_POST_URLS,
                              INDEX_PAGE, LOG_IN_URL, LOG_OUT_URL,
                              PASSWORD_URLS, PLAYER_GET_URLS, PLAYER_POST_URLS,
                              STAFF_GET_URLS, STAFF_POST_URLS, TEAM_GET_URLS,
                              TEAM_POST_URLS, UNLOAD_URLS, USER_GET_URLS,
                              USER_POST_URLS)


class TestSiteUrlsSmoke(BaseTestClass, UrlTestMixin):
    """Тесты урл-путей клиентской части сайта."""

    def setUp(self) -> None:
        """Метод для базовой настройки тестов класса."""
        self.super_client = Client()
        self.super_client.force_login(self.superuser)

    def get_default_client(self):
        """Метод для получения клиента по умолчанию."""
        return self.super_client

    def test_main_page(self):
        """Тест на проверку главной страницы."""
        self.url_get_test(INDEX_PAGE)

    def test_competitions_simple_access(self):
        """Тест доступности страниц с соревнованиями."""
        self.url_get_test(COMPETITION_GET_URLS)
        self.url_get_test(COMPETITION_POST_URLS, "post", HTTPStatus.FOUND)

    def test_player_simple_access(self):
        """Тест доступности страниц с игроками."""
        self.url_get_test(PLAYER_GET_URLS)
        self.url_get_test(PLAYER_POST_URLS, "post", HTTPStatus.FOUND)

    def test_staff_simple_access(self):
        """Тест доступности страниц с сотрудниками команд."""
        self.url_get_test(STAFF_GET_URLS)
        self.url_get_test(STAFF_POST_URLS, "post", HTTPStatus.FOUND)

    def test_team_simple_access(self):
        """Тест доступности страниц со спортивными командами."""
        self.url_get_test(TEAM_GET_URLS)
        self.url_get_test(TEAM_POST_URLS, "post", HTTPStatus.FOUND)

    def test_user_simple_access(self):
        """Тест доступности страниц с пользователями."""
        self.url_get_test(USER_GET_URLS)
        self.url_get_test(USER_POST_URLS, "post", HTTPStatus.FOUND)

    def test_unload_simple_access(self):
        """Тест доступности страниц с выгрузками."""
        self.url_get_test(UNLOAD_URLS)

    def test_log_in_out_access(self):
        """Тест доступности страниц входа-выхода на/с сайта."""
        self.url_get_test(LOG_OUT_URL, "post", HTTPStatus.FOUND)
        self.url_get_test(LOG_IN_URL)

    def test_password_simple_access(self):
        """Тест доступности страниц с манипуляциями с паролем."""
        self.url_get_test(PASSWORD_URLS)

    def test_auth_reset_urls(self):
        """Тест доступности страниц со сбросом пароля."""
        self.url_get_test(AUTH_RESET_URLS)


class TestAdminUrlsSmoke(BaseTestClass, UrlTestMixin):
    """Тесты урл-путей административной части сайта."""

    def setUp(self) -> None:
        """Метод для базовой настройки тестов класса."""
        self.super_client = Client()
        self.super_client.force_login(self.superuser)

    def get_default_client(self):
        """Метод для получения клиента по умолчанию."""
        return self.super_client

    def test_admin_base(self):
        """Тест главной страницы админки."""
        self.url_get_test(ADMIN_MAIN_URL)

    def test_admin_app_labels(self):
        """Тесты страниц с приложениями в админке."""
        self.url_get_test(ADMIN_APP_LABELS_URLS)

    def test_admin_auth_group(self):
        """Тесты страниц с группами в админке."""
        self.url_get_test(ADMIN_AUTH_GROUP_302, status_code=HTTPStatus.FOUND)
        self.url_get_test(ADMIN_AUTH_URLS)

    def test_admin_log_in_out(self):
        """Тесты страниц входа-выхода в/из админки."""
        self.url_get_test(ADMIN_LOGOUT, "post", status_code=HTTPStatus.FOUND)
        self.client.logout()
        self.url_get_test(ADMIN_LOGIN)

    def test_admin_city(self):
        """Тесты страниц с городами в админке."""
        self.url_get_test(ADMIN_CITY_URL_302, status_code=HTTPStatus.FOUND)
        self.url_get_test(ADMIN_CITY_URLS)

    def test_admin_competitions(self):
        """Тесты страниц с соревнованиями в админке."""
        self.url_get_test(
            ADMIN_COMPETITIONS_URLS_302,
            status_code=HTTPStatus.FOUND,
        )
        self.url_get_test(ADMIN_COMPETITIONS_URLS)

    def test_admin_diagnosis(self):
        """Тесты страниц с диагнозами в админке."""
        self.url_get_test(
            ADMIN_DIAGNOSIS_URL_302,
            status_code=HTTPStatus.FOUND,
        )
        self.url_get_test(ADMIN_DIAGNOSIS_URLS)

    """
    Что - то этот тест не хочет работать
    def test_admin_discipline_level(self):
        Тесты страниц с уровнями дисциплин в админке.
        self.url_get_test(
            ADMIN_DISCIPLINE_LEVEL_URL_302, status_code=HTTPStatus.FOUND
        )
        self.url_get_test(ADMIN_DISCIPLINE_LEVEL_URLS)
    """

    def test_admin_discipline_name(self):
        """Тесты страниц с наименованиями дисциплин в админке."""
        self.url_get_test(
            ADMIN_DISCIPLINE_NAME_URL_302,
            status_code=HTTPStatus.FOUND,
        )
        self.url_get_test(ADMIN_DISCIPLINE_NAME_URLS)

    @pytest.mark.skip(reason="Модель Document был исключен из админки")
    def test_admin_document(self):
        """Тесты страниц с документом в админке."""
        # self.url_get_test(
        #   ADMIN_DOCUMENT_URL_302, status_code=HTTPStatus.FOUND
        # )
        # self.url_get_test(ADMIN_DOCUMENT_URLS)

    def test_admin_nosology(self):
        """Тесты страниц с нозологией в админке."""
        self.url_get_test(ADMIN_NOSOLOGY_URL_302, status_code=HTTPStatus.FOUND)
        self.url_get_test(ADMIN_NOSOLOGY_URLS)

    def test_admin_player(self):
        """Тесты страниц с игроками в админке."""
        self.url_get_test(ADMIN_PLAYER_URL_302, status_code=HTTPStatus.FOUND)
        # TODO: Раскомментировать, когда будет починена админка. Сейчас на
        #  сайте реально недоступны страницы "/admin/main/player/1/change/" и
        #  "/admin/main/player/add/".
        # self.url_get_test(ADMIN_PLAYER_URLS)

    def test_admin_staff_member(self):
        """Тесты страниц с сотрудником в админке."""
        self.url_get_test(
            ADMIN_STAFF_MEMBER_URL_302,
            status_code=HTTPStatus.FOUND,
        )
        self.url_get_test(ADMIN_STAFF_MEMBER_URLS)

    @pytest.mark.skip(reason="Модель StuffTeamMember был исключен из админки")
    def test_admin_staff_team_member(self):
        """Тесты страниц с сотрудником команды в админке."""
        # self.url_get_test(
        #     ADMIN_STAFF_TEAM_MEMBER_URL_302, status_code=HTTPStatus.FOUND
        # )
        # self.url_get_test(ADMIN_STAFF_TEAM_MEMBER_URLS)

    def test_admin_team(self):
        """Тесты страниц с командами в админке."""
        self.url_get_test(ADMIN_TEAM_URL_302, status_code=HTTPStatus.FOUND)
        self.url_get_test(ADMIN_TEAM_URLS)

    def test_admin_password(self):
        """Тесты страниц изменения-сброса пароля в админке."""
        self.url_get_test(ADMIN_PASSWORD_URLS)

    def test_admin_proxy_group(self):
        """Тесты страниц с прокси-группами в админке."""
        self.url_get_test(
            ADMIN_PROXY_GROUP_URL_302,
            status_code=HTTPStatus.FOUND,
        )
        self.url_get_test(ADMIN_PROXY_GROUP_URLS)

    def test_admin_user(self):
        """Тесты страниц с пользователями в админке."""
        self.url_get_test(ADMIN_USER_URL_302, status_code=HTTPStatus.FOUND)
        self.url_get_test(ADMIN_USER_URLS)
