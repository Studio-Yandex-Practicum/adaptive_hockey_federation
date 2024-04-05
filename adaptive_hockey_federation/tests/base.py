import copy
from http import HTTPStatus
from typing import Iterable

from competitions.models import Competition
from core import constants
from core.constants import ROLE_SUPERUSER
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from factory.django import DjangoModelFactory
from main.data_factories.factories import (
    CompetitionFactory,
    DiagnosisFactory,
    DisciplineNameFactory,
    DocumentFactory,
    PlayerFactory,
    StaffTeamMemberFactory,
    TeamFactory,
)
from main.models import (
    Diagnosis,
    DisciplineName,
    Document,
    Player,
    StaffTeamMember,
    Team,
)
from tests.fixture_user import test_role_user
from tests.url_test import TEST_GROUP_NAME
from tests.utils import render_url
from users.factories import UserFactory
from users.models import ProxyGroup, User

URL_MSG = (
    "{method} запрос по адресу: {msg_url} должен вернуть ответ со статусом "
    "{status_code}. Тестировался запрос по адресу: {url}"
)
TEST_SETUP_ERROR = "Неверные настройки теста:"


class BaseTestClass(TestCase):
    """Базовый класс для тестирования.
    При инициализации создает в тестовой БД по одному экземпляру каждой из
    задействованных в приложении моделей. Пользователей создается два:
    суперпользователь и обычный пользователь."""

    superuser: User
    user: User
    discipline_name: DisciplineName
    team: Team
    diagnosis: Diagnosis
    player: Player
    staff: StaffTeamMember
    competition: Competition
    document: Document

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        ProxyGroup.objects.create(name=TEST_GROUP_NAME).save()
        constants.GROUPS_BY_ROLE[test_role_user] = TEST_GROUP_NAME
        cls.superuser = User.objects.create_user(
            password="super1234",
            first_name="Супер",
            last_name="Пользователь",
            role=ROLE_SUPERUSER,
            email="superuser@fake.fake",
            is_staff=True,
            is_superuser=True,
        )
        cls.user = UserFactory.create(role=test_role_user)
        cls.discipline_name = DisciplineNameFactory.create()
        cls.team = TeamFactory.create()
        cls.competition = CompetitionFactory.create()
        cls.diagnosis = DiagnosisFactory.create()
        cls.player = PlayerFactory.create()
        cls.staff = StaffTeamMemberFactory.create()
        cls.document = DocumentFactory.create(player=cls.player)


class UrlTestMixin:
    """Миксин предоставляет унифицированный метод для тестирования
    урл-адресов, с генерацией информативного сообщения."""

    def get_default_client(self) -> Client:
        """Переопределите этот метод для тестирования по умолчанию клиентом,
        отличным от простого неавторизованного."""
        return getattr(self, "client")

    def url_get_test(
        self,
        urls: Iterable | str,
        method: str = "get",
        status_code: int = HTTPStatus.OK,
        subs: tuple[str, ...] | str = "1",
        client: Client | None = None,
        message: str | None = None,
    ):
        """Унифицированный метод для урл-тестов.
        - urls: урл-адрес либо список или кортеж урл-адресов, подлежащих
          тестированию;
        - method: метод запроса (обычно "get" или "post", по умолчанию -
          "get");
        - status_code: ожидаемый ответ, по умолчанию - 200.
        - subs: строка или кортеж строк подстановки вместо
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
        - client: клиент для тестирования.
          Если не определить этот параметр, то клиент будет получен из
          метода get_default_client(). Если метод get_default_client() не
          переопределен в классе, то тестирование будет проводиться с
          простым неавторизованным клиентом.
        - message: кастомное сообщение в случае непрохождения теста,
          если генерируемое методом сообщение по каким-то причинам не
          устраивает.
        """
        client = client or self.get_default_client()
        if isinstance(urls, str) or isinstance(urls, dict):
            urls = (urls,)
        for url in urls:
            if isinstance(url, dict):
                url = url["url"]
            url_for_message = url
            url = render_url(url, subs)
            msg = message or URL_MSG.format(
                method=method.upper(),
                msg_url=url_for_message,
                status_code=status_code,
                url=url,
            )
            with self.__getattribute__("subTest")(url=url):
                response = client.__getattribute__(method.lower())(url)
                self.__getattribute__("assertEqual")(
                    response.status_code,
                    status_code,
                    msg=msg,
                )


class ModelTestBaseClass(BaseTestClass):
    model: type[Model] | None = None
    model_schema: dict | None = None
    model_factory: DjangoModelFactory | None = None

    assertEqual = TestCase.assertEqual
    assertTrue = TestCase.assertTrue
    assertFalse = TestCase.assertFalse
    assertRaises = TestCase.assertRaises
    subTest = TestCase.subTest

    def get_model(self):
        if self.model:
            return self.model
        raise Exception(
            f"{TEST_SETUP_ERROR} не определено поле model в "
            f"классе {__class__}."
        )

    @property
    def future_obj_id(self):
        return self.get_model().objects.count() + 1

    def get_model_schema(self):
        if self.model_schema:
            return self.model_schema
        raise Exception(
            f"{TEST_SETUP_ERROR} не определено поле model_schema в классе"
            f" {self.__class__.__name__}."
        )

    def _get_schema_key_value(self, key_name: str, schema: dict | None = None):
        schema = schema or self.get_model_schema()
        if value := schema.get(key_name, None):
            return value
        raise Exception(
            f"{TEST_SETUP_ERROR} в предоставленной схеме '{self.get_model()}' "
            f"класса '{self.__class__.__name__} 'отсутствует ключ "
            f"'{key_name}'."
        )

    def get_correct_create_schema(self):
        schema = copy.copy(self._get_schema_key_value("correct_create"))
        self.fill_foreign_keys(schema)
        return schema

    def get_correct_update_schema(self):
        schema = copy.copy(self._get_schema_key_value("correct_update"))
        self.fill_foreign_keys(schema)
        return schema

    def get_must_not_be_admitted_schemas(self):
        return self._get_schema_key_value("must_not_be_admitted")

    def get_must_be_admitted_schema(self):
        return self._get_schema_key_value("must_be_admitted")

    def create(self, **kwargs):
        if self.model_factory:
            return self.model_factory.create(**kwargs)
        obj = self.model.objects.create(**kwargs)
        obj.save()
        return obj

    def _post(self, url, **kwargs):
        self.client.force_login(self.superuser)
        return self.client.post(url, kwargs)

    def try_to_create_via_url(self, url, **kwargs):
        self.replace_foreign_keys(kwargs)
        try:
            return self._post(url, **kwargs)
        except Exception as e:
            raise AssertionError(
                f"При создании объекта модели"
                f" {self.get_model().__name__} "
                f"путем пост-запроса на адрес '{url}' c "
                f"корректными данными возникает исключение '{e}'. "
                f"Использовались следующие данные: {kwargs}"
            )

    @staticmethod
    def replace_foreign_keys(fields_kwargs: dict):
        for key, value in fields_kwargs.items():
            if isinstance(value, Model):
                fields_kwargs[key] = getattr(value, "id")

    @staticmethod
    def fill_foreign_keys(fields_kwargs: dict):
        for key, value in fields_kwargs.items():
            # if isinstance(value, type(Model)):
            if type(value) is type(Model):
                fk_obj = value.objects.first()  # noqa
                fields_kwargs[key] = fk_obj

    def try_to_update_via_url(self, url, **kwargs):
        self.replace_foreign_keys(kwargs)
        try:
            return self._post(url, **kwargs)
        except Exception as e:
            raise AssertionError(
                f"При изменении объекта модели"
                f" {self.get_model().__name__} "
                f"путем пост-запроса на адрес '{url}' "
                f"возникает исключение '{e}'. "
                f"Использовались следующие данные: {kwargs}"
            )

    def try_to_delete_via_url(self, url, **kwargs):
        try:
            return self._post(url, **kwargs)
        except Exception as e:
            raise AssertionError(
                f"При удалении объекта модели"
                f" {self.get_model().__name__} "
                f"путем пост-запроса на адрес '{url}' возникает исключение "
                f"'{e}'."
            )

    @transaction.atomic()
    def try_to_create(self, **kwargs):
        try:
            obj = self.create(**kwargs)
            obj.full_clean()
            return obj
        except Exception as e:
            raise AssertionError(
                f"При создании объекта модели {self.get_model().__name__} с "
                f"корректными данными возникает исключение '{e}'. "
                f"Использовались следующие данные: {kwargs}"
            )

    @transaction.atomic()
    def try_to_delete(self, obj_id):
        model = self.get_model()
        try:
            obj = get_object_or_404(model, id=obj_id)
            obj.delete()
        except Exception as e:
            raise AssertionError(
                f"При попытке удаления из БД записи о заведомо существующем "
                f"объекте модели {self.get_model().__name__} "
                f"возникает исключение '{e}'. "
                f"Использовались следующие данные: id={obj_id}"
            )

    def update(self, obj: Model, **kwargs):
        for field, value in kwargs.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        obj.full_clean()
        obj.save()

    def try_to_update(self, obj: Model, **kwargs):
        try:
            self.update(obj, **kwargs)
        except Exception as e:
            raise AssertionError(
                f"При обновлении объекта модели "
                f"{self.get_model().__name__} с "
                f"корректными данными возникает исключение '{e}'."
                f"Использовались следующие данные: {kwargs}"
            )

    def objects_count_test(self, estimated_count: int, err_msg: str):
        count = self.get_model().objects.count()
        self.assertEqual(count, estimated_count, msg=err_msg)

    def is_exists(self, **obj_kwargs):
        return self.get_model().objects.filter(**obj_kwargs).exists()

    def assert_object_exist(self, err_msg: str, **obj_kwargs):
        if obj_kwargs.get("password", None):
            obj_kwargs.pop("password")
        self.assertTrue(self.is_exists(**obj_kwargs), err_msg)

    def assert_object_not_exist(self, err_msg: str, **obj_kwargs):
        if obj_kwargs.get("password", None):
            obj_kwargs.pop("password")
        self.assertFalse(self.is_exists(**obj_kwargs), err_msg)

    def correct_create_tests(
        self, model_correct_schema: dict | None = None, url: str | None = None
    ):
        schema = model_correct_schema or self.get_correct_create_schema()
        initial_objects_count = self.get_model().objects.count()
        via_url = ""
        if url:
            self.try_to_create_via_url(url, **schema)
            via_url = f" через POST-запрос по адресу: {url}"
        else:
            self.try_to_create(**schema)

        err_msg = (
            f"При создании объекта модели "
            f"'{self.get_model().__name__}'{via_url} новое количество "
            f"объектов в БД не соответствует ожидаемому. Ожидаемое "
            f"количество объектов в БД: {initial_objects_count + 1}."
        )
        self.objects_count_test(initial_objects_count + 1, err_msg=err_msg)

        err_msg = (
            f"После создания объекта модели "
            f"'{self.get_model().__name__}'{via_url} объект с данными, "
            f"использованным для создания, не обнаруживается в БД. "
            f"Объект создавался со следующими данными: {schema}."
        )
        self.assert_object_exist(err_msg, **schema)

    def correct_update_tests(self, url: str | None = None, **kwargs):
        cr_schema = self.get_correct_create_schema()
        upd_schema = self.get_correct_update_schema()
        obj = self.try_to_create(**cr_schema)
        via_url = ""
        if url:
            self.try_to_update_via_url(url, **upd_schema, **kwargs)
            via_url = f" через POST-запрос по адресу: {url}"
        else:
            self.try_to_update(obj, **upd_schema)
        err_msg = (
            f"После обновления объекта модели "
            f"{self.get_model().__name__}{via_url}, объект с корректными "
            f"данными, использованным для обновления, не обнаруживается в БД. "
            f"Объект обновлялся со следующими данными: {upd_schema}."
        )
        self.assert_object_exist(err_msg, **upd_schema)

    def correct_delete_tests(self, url: str | None = None, **kwargs):
        cr_schema = self.get_correct_create_schema()
        obj = self.try_to_create(**cr_schema)
        initial_objects_count = self.get_model().objects.count()
        id = obj.id
        via_url = ""
        if url:
            self.try_to_delete_via_url(url, **kwargs)
            via_url = f" через POST-запрос по адресу: {url}"
        else:
            self.try_to_delete(id)
        err_msg = (
            f"После удаления объекта модели "
            f"{self.get_model().__name__}{via_url} количество объектов в БД "
            f"не соответствует ожидаемому."
        )
        self.objects_count_test(initial_objects_count - 1, err_msg=err_msg)

    def update_field(
        self, obj: Model, msg, url: str | None = None, **field_kwargs
    ):
        if url:
            schema = self.get_correct_update_schema()
            schema.update(field_kwargs)
            self.try_to_update_via_url(url, **schema)
        else:
            self.update(obj, **field_kwargs)

    def correct_field_test(
        self, obj: Model, msg, url: str | None = None, **kwargs
    ):
        if url:
            self.try_to_update_via_url(url, **kwargs)
        else:
            self.update(obj, **kwargs)

    @staticmethod
    def _unpack_test_values(field, value):
        res = []
        value = list(value)
        msg = value.pop()
        if any(tuple_val := tuple(isinstance(i, tuple) for i in value)):
            tuple_index = (1, 0)[tuple_val[0]]
            prior_val = value[0] if tuple_index else ""
            post_val = value[-1] if (len(value) - 1) > tuple_index else ""
            batch_value = []
            for item in value[tuple_index]:
                batch_value.append(
                    {
                        "msg": msg,
                        "value": prior_val + item + post_val,
                        "field": field,
                    }
                )
            res.append(batch_value)
        else:
            res.append({"msg": msg, "value": value[0], "field": field})
        return res

    def _unpack_field_tests(self, test_item: dict):
        fields = self._get_schema_key_value("fields", test_item)
        value_set = self._get_schema_key_value("test_values", test_item)
        if isinstance(fields, str):
            fields = (fields,)
        unpacked_tests = []
        for field in fields:
            for value in value_set:
                for unpacked_value in self._unpack_test_values(field, value):
                    unpacked_tests.append(unpacked_value)
        return unpacked_tests

    @staticmethod
    def _alter_tested_value_info(value, force_value):
        if value or force_value:
            return f"Тестировавшееся значение: '{value}'"
        return ""

    def _incorrect_field_msg_compile(
        self, field, msg, value=None, force_value=True
    ):
        tested_value_info = self._alter_tested_value_info(value, force_value)
        return (
            f"Проверьте, что при попытке сохранения в БД модели"
            f" {self.get_model().__name__} с полем {field}, "
            f"содержащим невалидные данные ({msg}), "
            f"вызывается исключение ValidationError. {tested_value_info}"
        ).strip()

    def _incorrect_field_via_url_msg_compile(
        self, field, msg, url, value=None, force_value=True
    ):
        tested_value_info = self._alter_tested_value_info(value, force_value)
        return (
            f"Проверьте, что POST-запрос по адресу {url}  "
            f"содержащий невалидные данные для поля {field} модели"
            f" {self.get_model().__name__} ({msg}), "
            f"возвращает ответ со статус-кодом 200(OK) или 302(FOUND) и "
            f"объект в БД не изменяется."
            f" {tested_value_info}"
        ).strip()

    def _correct_field_msg_compile(
        self, field, msg, url, value=None, force_value=True
    ):
        tested_value_info = self._alter_tested_value_info(value, force_value)
        if url:
            return self._correct_field_via_url_msg_compile(
                field, msg, url, value, force_value
            )
        return (
            f"Проверьте, в поле {field} модели {self.get_model().__name__} "
            f"допускается сохранение и не вызывает ошибки валидации такие "
            f"валидные данные, как {msg}. {tested_value_info}"
        ).strip()

    def _correct_field_via_url_msg_compile(
        self, field, msg, url, value=None, force_value=True
    ):
        tested_value_info = self._alter_tested_value_info(value, force_value)
        return (
            f"Проверьте, что POST-запрос по адресу '{url}'  "
            f"содержащий такие валидные данные для поля '{field}' модели "
            f"'{self.get_model().__name__}', как '{msg}', "
            f"возвращает ответ со статус-кодом 200(OK) или 302(FOUND) и "
            f"изменения сохраняются в БД. {tested_value_info}"
        ).strip()

    def _incorrect_field_sub_test_via_url(
        self, url, test, sub: bool = True, **kwargs
    ):
        field, value, msg = test["field"], test["value"], test["msg"]
        field_kwargs = {field: value}
        schema = self.get_correct_update_schema()
        schema.update(field_kwargs)
        err_msg = (
            f"Проверьте, что POST-запрос по адресу {url}  "
            f"содержащий невалидные данные для поля {field} модели"
            f" {self.get_model().__name__} ({msg}), "
            f"возвращает ответ со статус-кодом 200(OK) или 302(FOUND)."
            f" {self._alter_tested_value_info(value, True)}"
        ).strip()
        response = self.try_to_update_via_url(url, **schema, **kwargs)
        self.assertIn(
            response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND], err_msg
        )
        err_msg = (
            f"В результате POST-запроса по адресу {url}  "
            f"содержащего невалидные данные для поля {field} модели "
            f"{self.get_model().__name__} ({msg}), "
            f"объект с указанными невалидными данными обнаруживается в "
            f"БД. {self._alter_tested_value_info(value, True)}"
        ).strip()
        if sub:
            with self.subTest(msg=err_msg):
                self.assert_object_not_exist(msg, **schema)
        else:
            self.assert_object_not_exist(err_msg, **schema)

    def _incorrect_field_sub_test(self, test, obj, sub, url=None):
        field = test["field"]
        msg = test["msg"]
        value = test["value"]
        msg = self._incorrect_field_msg_compile(field, msg, value)
        kwargs = {test["field"]: test["value"]}

        def _inner_assert():
            with transaction.atomic():
                self.assertRaises(
                    ValidationError,
                    self.update_field,
                    obj,
                    msg,
                    url,
                    **kwargs,
                )

        if sub:
            with self.subTest(msg=msg):
                _inner_assert()
        else:
            self.update_field(obj=obj, msg=msg, url=url, **kwargs)
        # Приводим объект в заведомо валидное состояние.
        self.try_to_update(obj, **self.get_correct_create_schema())

    def _get_field_tests_set(
        self, schemas: Iterable, create_obj: bool = True
    ) -> tuple | tuple[tuple, Model]:
        tests_set = []
        for test_item in schemas:
            tests_set += self._unpack_field_tests(test_item)
        if create_obj:
            obj = self.try_to_create(**self.get_correct_create_schema())
            return tuple(tests_set), obj
        return tuple(tests_set)

    def incorrect_field_tests_via_url(self, url: str, **kwargs):
        schemas = self.get_must_not_be_admitted_schemas()
        tests_set, _ = self._get_field_tests_set(schemas, create_obj=True)
        for batch_test in tests_set:
            if isinstance(batch_test, dict):
                self._incorrect_field_sub_test_via_url(
                    url, batch_test, **kwargs
                )
            else:
                for test in batch_test:
                    assertion_error = None
                    try:
                        self._incorrect_field_sub_test_via_url(
                            url, test, sub=False, **kwargs
                        )
                    except AssertionError as e:
                        err_msg = e.args[0]
                        with self.subTest(msg=err_msg):
                            assertion_error = e
                            raise e
                    finally:
                        if assertion_error:
                            break

    def incorrect_field_tests(self, url: str | None = None):
        schemas = self.get_must_not_be_admitted_schemas()
        tests_set, obj = self._get_field_tests_set(schemas, create_obj=True)
        for batch_test in tests_set:
            if isinstance(batch_test, dict):
                self._incorrect_field_sub_test(
                    test=batch_test, obj=obj, sub=True, url=url
                )
            else:
                for test in batch_test:
                    msg = self._incorrect_field_msg_compile(
                        test["field"], test["msg"], test["value"]
                    )
                    exception = None
                    try:
                        self._incorrect_field_sub_test(
                            test=test, obj=obj, sub=False, url=url
                        )
                    except Exception as e:
                        exception = e
                    finally:
                        with self.subTest(msg=msg):
                            with self.assertRaises(ValidationError):
                                if exception:
                                    raise exception
                            continue
                    break

    def correct_field_tests(self, url: str | None = None, **kwargs):
        schema = self.get_must_be_admitted_schema()
        correct_schema = self.get_correct_create_schema()
        obj = self.try_to_create(**correct_schema)
        correct_schema.update(kwargs)
        tests_set = []
        for test_item in schema:
            tests_set += self._unpack_field_tests(test_item)
        for batch_test in tests_set:
            if isinstance(batch_test, dict):
                batch_test = (batch_test,)
            for test in batch_test:
                kwargs = {test["field"]: test["value"]}
                msg = self._correct_field_msg_compile(**test, url=url)
                update_schema = copy.copy(correct_schema)
                update_schema.update(kwargs)
                with self.subTest(msg=msg):
                    self.correct_field_test(obj, msg, url, **update_schema)
                    self.assertTrue(
                        self.get_model().objects.filter(**kwargs).exists(),
                        msg=msg,
                    )
