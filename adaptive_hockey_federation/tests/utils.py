import re
from http import HTTPStatus
from typing import Any

from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from users.models import User


class UrlToTest:
    """
    Класс для использования в автоматизации тестирования урлов.

    В настоящем виде, в зависимости от параметров, может проводить тесты (
    возвращать пару "фактический ответ - ожидаемый ответ" и сообщение) на:
        - возвращаемый ответ для авторизованного пользователя;
        - возвращаемый ответ для неавторизованного пользователя;
        - возвращаемый ответ для пользователя, обладающего определенным
        разрешением;
        - возвращаемый ответ для пользователя, НЕ обладающего определенным
        разрешением;
        - возвращаемый ответ для пользователя - администратора;
        - возвращаемый ответ для пользователя - НЕ администратора.


    Параметры создания объекта:
        url - соответствующий урл;
        code_estimated - код статуса или список кодов статуса, который в норме
            должна возвращать страница. По умолчанию - HTTPStatus.OK (200);
        permission_required: - разрешение (permission), требующееся для
            соответствующего урла. Принимает строку с codename
            соответствующего разрешения (например 'change_user'). В случае
            permission_required==None метод execute_tests проведет
            только тесты на авторизованного/неавторизованного пользователя.
            Если указать конкретное разрешение (permission codename),
            то будет проведен тест на ответ неавторизованному пользователю,
            а также отдельно - на ответы авторизованному пользователю,
            обладающему соответствующим разрешением, и авторизованному
            пользователю, не обладающему таким разрешением.
            По умолчанию = None;
        authorized_only:
            == True - тест на неавторизованного пользователя будет ожидать
            ответ или один из ответов, указанных в параметре
            "unauthorized_code_estimated",
            == False (по умолчанию) - тест на неавторизованного пользователя
            будет ожидать такой же ответ, как и для авторизованного
            пользователя (code_estimated);
        unauthorized_code_estimated:
            Код статуса или список кодов, которые в норме должна возвращать
            страница для неавторизованного пользователя в том случае,
            когда параметр "authorized_only" равен True. При
            authorized_only==False данный параметр не используется.
            По умолчанию - HTTPStatus.FOUND(302);
        admin_only:
            ==False (по умолчанию) - проводятся стандартные тесты на
            авторизованного/неавторизованного пользователя.
            ==True - вместо стандартного теста на
            авторизованного пользователя будут проведены два
            теста: на ответы авторизованному пользователю, обладающему
            полномочиями администратора, и авторизованному пользователю,
            не обладающему такими полномочиями;
        use_post:
            == False (по умолчанию)
            == True - передавать такое значение следует только для url,
            чей view наследуется от LogoutView, чтобы не отображался
            warning, связанный с устареванием метода "get" для выхода
            пользователя в Django 5.0, либо в иных случаях, когда необходимо
            протестировать post-запросы к странице;
        path_render_subs:
            строка или кортеж строк подстановки вместо
            динамических идентификаторов объектов типа <int:pk> в урл-путях.
            Например, для обработки пути:
            "/competitions/<int:competition_id>/teams/<int:pk>/add/"
            если передать кортеж ("1", "2"), то он преобразует путь в
            "/competitions/1/teams/2/add/").
            Если подстановок больше, чем элементов в кортеже "subs", то для
            оставшихся подстановок возьмется последний элемент. Если в примере
            выше передать строку "1" или кортеж ("1",), то урл преобразуется в
            "/competitions/1/teams/1/add/". Если в урл нет динамических
            идентификаторов, данный параметр не имеет значения.
    """

    def __init__(
        self,
        url: str,
        *,
        code_estimated: int | list | tuple = HTTPStatus.OK,
        permission_required: str | None = None,
        authorized_only: bool = True,
        unauthorized_code_estimated: int | list | tuple = HTTPStatus.FOUND,
        admin_only: bool = False,
        use_post: bool = False,
        path_render_subs: str | tuple[str, ...] | list[str] = "1",
    ):
        """
        Метод инициализации экземпляра класса.

        Присваивает необходимые атрибуты.
        """
        self.path = url
        self.authorized_only = authorized_only
        self.code_estimated = code_estimated
        self.permission = None
        self.admin_only = admin_only
        if permission_required:
            try:
                self.permission = Permission.objects.get(
                    codename=permission_required,
                )
            except ObjectDoesNotExist:
                raise AssertionError(
                    f"!!! Выполнить тесты для урл: {self.path} "
                    f"невозможно. Проверьте, что в базе данных предусмотрено "
                    f"разрешение '{permission_required}'.!!!",
                )

        if self.authorized_only:
            self.unauthorized_code = unauthorized_code_estimated
        else:
            self.unauthorized_code = HTTPStatus.OK
        self.use_post = use_post
        self.request_method = ("GET", "POST")[self.use_post]
        self.path_for_message = f"{self.request_method}-запрос по адресу {url}"
        self.path = render_url(url, path_render_subs)

    def _get_response(self, client: Client):
        if self.use_post:
            return client.post(self.path)
        return client.get(self.path)

    def _get_auth_response(
        self,
        client: Client,
        user: User,
        clear_permissions: bool = True,
        clear_admin: bool = True,
    ):
        if clear_permissions:
            user.user_permissions.clear()
        if user.is_staff and clear_admin:
            user.is_staff = False
            user.save()
        client.force_login(user)
        return self._get_response(client)

    def unauthorized_test(self, client: Client) -> tuple[int, Any, str]:
        """
        Возвращает "ответ-ожидание" для неавторизованного пользователя.

        Последним значением возвращает сообщение, которое можно использовать
        в тестах.
        """
        client.logout()
        response = self._get_response(client)
        message = (
            f"Для неавторизованного пользователя "
            f"{self.path_for_message} должен вернуть ответ со статусом "
            f"{self.unauthorized_code}."
        )
        return response.status_code, self.unauthorized_code, message

    def user_with_permission_test(self, client: Client, user: User):
        """
        Возвращает "ответ-ожидание" для авторизованного пользователя.

        Для авторизованного пользователя, обладающего разрешением с codename,
        сохраненным в self.permission.
        Последним значением возвращает сообщение, которое можно использовать
        в тестах.
        """
        if isinstance(self.permission, Permission):
            user.user_permissions.add(self.permission)
        else:
            raise Exception("Ошибка при определении разрешения.")
        response = self._get_auth_response(client, user, False)
        message = (
            f"Для пользователя, обладающего разрешением "
            f"{self.permission.codename}, {self.path_for_message} "
            f"должен вернуть ответ со статусом "
            f"{self.code_estimated}."
        )
        return response.status_code, self.code_estimated, message

    def authorized_test(self, client: Client, user: User):
        """
        Возвращает "ответ-ожидание" для авторизованного пользователя.

        Для авторизованного пользователя без каких-либо специфических
        разрешений.
        """
        response = self._get_auth_response(client, user)
        message = (
            f"Для любого авторизованного пользователя, "
            f"{self.path_for_message} должен вернуть ответ со "
            f"статусом {self.code_estimated}."
        )
        return response.status_code, self.code_estimated, message

    def user_without_permission_test(self, client: Client, user: User):
        """
        Возвращает "ответ-ожидание" для авторизованного пользователя.

        Для авторизованного пользователя, НЕ обладающего разрешением с
        codename, сохраненным в self.permission.
        Последним значением возвращает сообщение, которое можно использовать
        в тестах.
        """
        response = self._get_auth_response(
            client,
            user,
            clear_permissions=True,
        )
        if isinstance(self.permission, Permission):
            codename = self.permission.codename
        else:
            codename = ""
        message = (
            f"Для пользователя, не обладающего разрешением "
            f"{codename}, {self.path_for_message} "
            f"должен вернуть ответ со статусом "
            f"{HTTPStatus.FORBIDDEN}."
        )
        return response.status_code, HTTPStatus.FORBIDDEN, message

    def admin_test(self, client: Client, user: User):
        """
        Возвращает "ответ-ожидание" для авторизованного пользователя.

        Для авторизованного пользователя, обладающего полномочиями
        администратора (is_staff=true).
        Последним значением возвращает сообщение, которое можно использовать
        в тестах.
        """
        user.is_staff = True
        user.save()
        response = self._get_auth_response(client, user, clear_admin=False)
        message = (
            f"Для пользователя, являющегося администратором (is_staff=True) "
            f"{self.path_for_message} должен вернуть ответ со "
            f"статусом {self.code_estimated}."
        )
        return response.status_code, self.code_estimated, message

    def non_admin_test(self, client: Client, user: User):
        """
        Возвращает "ответ-ожидание" для авторизованного пользователя.

        Для авторизованного пользователя, НЕ обладающего полномочиями
        администратора (is_staff=False).
        Последним значением возвращает сообщение, которое можно использовать
        в тестах.
        """
        response = self._get_auth_response(client, user)
        message = (
            f"Для пользователя, НЕ являющегося администратором ("
            f"is_staff=False) {self.path_for_message} должен вернуть "
            f"ответ с одним из статусов "
            f"{HTTPStatus.FOUND, HTTPStatus.MOVED_PERMANENTLY}."
        )
        return (
            response.status_code,
            (HTTPStatus.FOUND, HTTPStatus.MOVED_PERMANENTLY),
            message,
        )

    def execute_tests(self, client: Client, user: User):
        """
        Основной метод класса.

        Возвращает список кортежей (ответ, ожидаемый ответ, сообщение)
        для всех вариантов GET-запросов к конкретному url.
        """
        res = [self.unauthorized_test(client)]
        if self.permission and isinstance(self.permission, Permission):
            res.append(self.user_with_permission_test(client, user))
            res.append(self.user_without_permission_test(client, user))
        elif not self.admin_only:
            res.append(self.authorized_test(client, user))

        if self.admin_only:
            res.append(self.admin_test(client, user))
            res.append(self.non_admin_test(client, user))

        return res


def render_url(url: str, subs: tuple | str | list):
    pattern = re.compile(r"<[^/]+>")
    if not re.search(pattern, url):
        return url
    if isinstance(subs, str):
        subs = (subs,)
    for sub in subs:
        url = re.sub(pattern, sub, url, count=1)
    if re.search(pattern, url):
        url = re.sub(pattern, subs[-1], url)
    return url
