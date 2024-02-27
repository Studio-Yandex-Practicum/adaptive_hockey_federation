from http import HTTPStatus
from typing import Any

from django.contrib.auth.models import Permission
from django.test import Client
from users.models import User


class UrlToTest:
    """Класс для использования в автоматизации тестирования урлов.

    В настоящем виде может проводить тесты (возвращать пару "фактический
    ответ - ожидаемый ответ" и сообщение) на:
        - возвращаемый ответ для авторизованного пользователя;
        - возвращаемый ответ для неавторизованного пользователя;
        - возвращаемый ответ для пользователя, обладающего определенным
        разрешением;
        - возвращаемый ответ для пользователя, НЕ обладающего определенным
        разрешением.

    Параметры создания объекта:
        path - соответствующий урл,
        code_estimated - код статуса или список кодов статуса, который в норме
            должна возвращать страница. По умолчанию - HTTPStatus.OK (200),
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
            По умолчанию = None.
        authorized_only:
            == True - тест на неавторизованного пользователя будет ожидать
            ответ или один из ответов, указанных в параметре
            "unauthorized_code_estimated",
            == False (по умолчанию) - тест на неавторизованного пользователя
            будет ожидать такой же ответ, как и для авторизованного
            пользователя (code_estimated).
        unauthorized_code_estimated:
            Код статуса или список кодов, которые в норме должна возвращать
            страница для неавторизованного пользователя в том случае,
            когда параметр "authorized_only" равен True. При
            authorized_only==False данный параметр не используется.
            По умолчанию - HTTPStatus.FOUND(302).
    """

    def __init__(
        self,
        path: str,
        *,
        code_estimated: int | list | tuple = HTTPStatus.OK,
        permission_required: str | None = None,
        authorized_only: bool = True,
        unauthorized_code_estimated: int | list | tuple = HTTPStatus.FOUND,
    ):
        self.path = path
        self.authorized_only = authorized_only
        self.code_estimated = code_estimated
        self.permission = None
        if permission_required:
            self.permission = Permission.objects.get(
                codename=permission_required
            )
        if self.authorized_only:
            self.unauthorized_code = unauthorized_code_estimated
        else:
            self.unauthorized_code = HTTPStatus.OK

    def _get_auth_response(
        self, client: Client, user: User, clear_permissions: bool = True
    ):
        if clear_permissions:
            user.user_permissions.clear()
        client.force_login(user)
        return client.get(self.path)

    def unauthorized_test(self, client: Client) -> tuple[int, Any, str]:
        """Возвращает "ответ-ожидание" для неавторизованного пользователя.
        Последним значением возвращает сообщение, которое можно использовать
        в тестах."""
        client.logout()
        response = client.get(self.path)
        message = (
            f"Для неавторизованного пользователя страница {self.path} "
            f"должна вернуть ответ со статусом "
            f"{self.unauthorized_code}."
        )
        return response.status_code, self.unauthorized_code, message

    def user_with_permission_test(self, client: Client, user: User):
        """Возвращает "ответ-ожидание" для авторизованного пользователя,
        обладающего разрешением с codename, сохраненным в self.permission.
        Последним значением возвращает сообщение, которое можно использовать
        в тестах."""
        if isinstance(self.permission, Permission):
            user.user_permissions.add(self.permission)
        else:
            raise Exception("Ошибка при определении разрешения.")
        response = self._get_auth_response(client, user, False)
        message = (
            f"Для пользователя, обладающего разрешением "
            f"{self.permission.codename}, страница {self.path} "
            f"должна вернуть ответ со статусом "
            f"{self.code_estimated}."
        )
        return response.status_code, self.code_estimated, message

    def authorized_test(self, client: Client, user: User):
        """Возвращает "ответ-ожидание" для авторизованного пользователя без
        каких-либо специфических разрешений."""
        response = self._get_auth_response(client, user)
        message = (
            f"Для любого авторизованного пользователя, "
            f"страница {self.path} должна вернуть ответ со "
            f"статусом {self.code_estimated}."
        )
        return response.status_code, self.code_estimated, message

    def user_without_permission_test(self, client: Client, user: User):
        """Возвращает "ответ-ожидание" для авторизованного пользователя,
        НЕ обладающего разрешением с codename, сохраненным в self.permission.
        Последним значением возвращает сообщение, которое можно использовать
        в тестах."""
        response = self._get_auth_response(client, user)
        if isinstance(self.permission, Permission):
            codename = self.permission.codename
        else:
            codename = ""
        message = (
            f"Для пользователя, не обладающего разрешением "
            f"{codename}, страница {self.path} "
            f"должна вернуть ответ со статусом "
            f"{HTTPStatus.FORBIDDEN}."
        )
        return response.status_code, HTTPStatus.FORBIDDEN, message

    def execute_tests(self, client: Client, user: User):
        """Основной метод класса.
        Возвращает список кортежей (ответ, ожидаемый ответ, сообщение)
        для всех вариантов GET-запросов к конкретному url."""
        res = [self.unauthorized_test(client)]
        if self.permission and isinstance(self.permission, Permission):
            res.append(self.user_with_permission_test(client, user))
            res.append(self.user_without_permission_test(client, user))
        else:
            res.append(self.authorized_test(client, user))

        return res
