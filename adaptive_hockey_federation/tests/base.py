import copy
from http import HTTPStatus
from typing import Any, Iterable

from competitions.models import Competition
from core import constants
from core.constants import ROLE_SUPERUSER
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Model
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from factory.django import DjangoModelFactory  # type: ignore
from main.data_factories.factories import (
    CompetitionFactory,
    DiagnosisFactory,
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
    """Класс для CRUD-тестирования. Инициализация класса задана предком
    (BaseTestClass), который создает для каждого внутреннего тестового
    метода все необходимые фикстуры.

    1. Определите в классе - наследнике поля model и model_schema.

    Поле model - ссылка на класс соответствующей модели.

    Поле model_schema - схема тестирования. Оно должно представлять собой
    словарь с ключами:

        - "correct_create": словарь с парами "поле": "значение поля",
        которые будут использоваться как заведомо правильные значения полей
        для создания тестовых объектов. Минимально необходимый нобор полей
        для корректной работы - все обязательные поля. Остальные - по
        необходимости для нужд тестов. Для полей типа "ForeignKey",
        если они являются обязательными, надо указать ссылку на сам
        класс соответствующей модели, например "city": City. По умолчанию
        тест будет создавать объект с внешним ключом, в который запишет
        объект указанной модели, взятый методом first() (в приведенном
        примере - City.objects.first(). Необходимо позаботиться, чтобы хотя
        бы один такой объект существовал. Изменить это поведение можно,
        переопределив метод fill_foreign_keys();

        - "correct_update": аналогично ключу "correct_create". Данный ключ
        должен также содержать все обязательные поля, которые необходимы для
        создания нового объекта, поскольку запрос выполняется методом POST.
        Данный ключ будет использоваться для изменения тестовых объектов;

        - "must_not_be_admitted": кортеж со словарями для тестирования
        валидиации отдельных полей на предмет недопуска в БД невалидных
        значений.
            Словарь для тестирования валидации отдельных полей должен
            содержать два ключа:
                - "fields", значением которого может быть строка с названием
                тестируемого поля или кортеж из названий нескольких полей;
                - "test_values", значением которого является кортеж из
                одного или нескольких кортежей вида
                (
                    "тестовое НЕВАЛИДНОЕ значение",
                    "описание тестового значения"
                ).

            Пример формирования ключа "must_not_be_admitted": (
                    {"fields": ("name", "surname"),
                        "test_values": (
                            ("1234567890", "значение из цифр"),
                            ("Пётр1", "цифры наряду с буквами"),
                        ),
                    {"fields": "patronymic", "test_values" ...какие-нибудь
                    тесты для поля patronymic...
                )
            Обнаружив такой ключ, метод incorrect_field_tests
            поочередно для каждого поля проведет тесты на валидацию
            с указанными значениями, и вызовет AssertionError в том случае,
            если поле с таким значением не вызывает ошибки валидации.

            Для элемента test_values можно вместо одного значения указать
            также кортеж значений, тогда для каждого из указанных полей
            будут протестированы каждый иэ элементов возможных некорректных
            значений. Например, если в вышеуказанном примере вместо
            ("123456790", "значение из цифр") указать
            (tuple("1234567890"), "значение из цифр"), тест
            поочередно попытается присвоить полю значения "1", "2", "3" и т.д.,
            и при первом непройденном тесте остановит его и перейдет к
            тестированию значения "Пётр1". В этом же примере, опционально
            справа и (или) слева от кортежа можно добавить произвольные
            строковые значения, которые будут использоваться как префикс и
            постфикс в тесте. Например:
            ("Пётр ", tuple("1234567890"), " царь", "цифры наряду с буквами")
            будут тестировать валидацию значений:
                - "Пётр 1 царь";
                - "Пётр 2 царь";
                - "Пётр 3 царь" и т.д.
            Такие префикс и постфикс могут быть строго строковыми
            значениями, любой другой тип данных для них вызовет ошибку и(или)
            неправильную отработку тестов.

        - "must_be_admitted": то же самое, что и "must_not_be_admitted",
        но наоборот - здесь необходимо в качестве test_values
        указывать те значения, которые ДОЛЖНЫ являться валидными и
        сохраняться в БД штатно. Тест методом correct_field_tests()
        попытается изменить объект и выдаст ошибку, если объект с измененным
        значением не будет обнаружен.

    2. В классе предусмотрены следующие методы для
    тестирования:
        - correct_create_tests() - тест на создание объекта;
        - correct_update_tests() - тест на изменение объекта;
        - correct_delete_tests() - тест на удаление объекта;
        - incorrect_field_tests() - тест на защиту от невалидных данных
        отдельных полей;
        - incorrect_field_tests_via_url() - то же самое, но через url
        - correct_field_tests() - тест на допуск валидных значений в
        отдельные поля;

    !!! Вызов двух разных методов в одном тесте не рекомендуется, поскольку
    между ними в таком случае не будет производиться сброс тестовой БД к
    исходному состоянию, и результаты таких тестов могут быть некорректными !!!

    !!! Класс не предназначен для тестирования пермишенов, поэтому при
    тестировании CRUD через url по умолчанию все запросы выполняются от
    имени суперпользователя. Переопределить это поведение можно в методе
    _post(), хотя делать это не рекомендуется. !!!

    """

    model: type[Model] | None = None
    model_schema: dict | None = None
    model_factory: DjangoModelFactory | None = None

    def get_model(self):
        """Возвращает класс тестовой модели. Переопределите этот метод,
        если нужна другая логика."""
        if self.model:
            return self.model
        raise Exception(
            f"{TEST_SETUP_ERROR} не определено поле model в "
            f"классе {__class__}."
        )

    @property
    def future_obj_id(self):
        """Предсказывает id будущего объекта (для использования в
        тестировании CRUD через url, в котором указывается id записи."""
        return self.get_model().objects.count() + 1

    def get_model_schema(self):
        """Возвращает схему тестирования.
        Переопределение данного метода не рекомендуется. Для динамического
        добавления какого-то поля в схему создания или изменения объекта
        переопределите методы "get_correct_create_schema()" или
        "get_correct_update_schema"."""
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
        """Возвращает значение ключа "correct_create" схемы тестирования.
        Переопределите этот метод для изменения логики или динамического
        добавления какого-то поля в схему создания объекта."""
        schema = copy.copy(self._get_schema_key_value("correct_create"))
        self.fill_foreign_keys(schema)
        return schema

    def get_correct_update_schema(self):
        """Возвращает значение ключа "correct_update" схемы тестирования.
        Переопределите этот метод для изменения логики или динамического
        добавления какого-то поля в схему изменения объекта."""
        schema = copy.copy(self._get_schema_key_value("correct_update"))
        self.fill_foreign_keys(schema)
        return schema

    def get_must_not_be_admitted_schemas(self):
        """Возвращает значение ключа "must_not_be_admitted" схемы тестирования.
        Переопределите, если нужна другая логика."""
        return self._get_schema_key_value("must_not_be_admitted")

    def get_must_be_admitted_schema(self):
        """Возвращает значение ключа "must_be_admitted" схемы тестирования.
        Переопределите, если нужна другая логика."""
        return self._get_schema_key_value("must_be_admitted")

    def create(self, **kwargs):
        """Создает объект в БД.
        Параметр kwargs - словарь с парами "поле-значение"."""
        if self.model_factory:
            return self.model_factory.create(**kwargs)
        obj = self.model.objects.create(**kwargs)
        obj.save()
        return obj

    def _post(self, url, **kwargs):
        """Выполняет POST-запрос."""
        self.client.force_login(self.superuser)
        return self.client.post(url, kwargs)

    def try_to_create_via_url(self, url, **kwargs):
        """Пытается создать объект через url.
        Параметр kwargs - словарь с парами "поле-значение" для тела
        POST-запроса."""
        self.replace_foreign_keys_and_bools(kwargs)
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
    def replace_foreign_keys_and_bools(
        fields_kwargs: dict, replace_bools: bool = True
    ):
        """При создании или изменении объектов через url меняет ссылки на
        объекты БД на их id для корректного выполнения запроса. В этих же
        целях по умолчанию bool-значения полей меняются на строковые: True
        на "on", False - на пустую строку."""
        for key, value in fields_kwargs.items():
            if isinstance(value, Model):
                fields_kwargs[key] = getattr(value, "id")
            elif replace_bools and isinstance(value, bool):
                fields_kwargs[key] = ("", "on")[value]

    @staticmethod
    def fill_foreign_keys(fields_kwargs: dict):
        """Заменяет в схеме тестирования ссылки на модели ссылками на
        конкретные объекты модели в полях ForeignKey."""
        for key, value in fields_kwargs.items():
            if type(value) is type(Model):
                fk_obj = value.objects.first()  # noqa
                fields_kwargs[key] = fk_obj

    def try_to_update_via_url(self, url, **kwargs):
        """Пытается изменить объект через url.
        Параметр kwargs - словарь с парами "поле-значение" для тела
        POST-запроса.
        """
        self.replace_foreign_keys_and_bools(kwargs)
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
        """Пытается удалить объект через url.
        Параметр kwargs - словарь с парами "поле-значение" для тела
        POST-запроса.
        """
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
        """Пытается создать объект непосредственно в БД.
        Параметр kwargs - словарь с парами "поле-значение"."""
        str_kwargs = f"{kwargs}"
        try:
            obj = self.create(**kwargs)
            obj.full_clean()
            return obj
        except Exception as e:
            raise AssertionError(
                f"При создании объекта модели {self.get_model().__name__} с "
                f"корректными данными возникает исключение '{e}'. "
                f"Использовались следующие данные: {str_kwargs}"
            )

    @transaction.atomic()
    def try_to_delete(self, obj_id):
        """Пытается удалить объект с id "obj_id" непосредственно из БД.
        Для объектов, идентифицируемых по другому полю, переопределите этот
        метод."""
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

    @staticmethod
    def update(obj: Model, **kwargs):
        """Изменяет объект obj непосредственно в БД."""
        for field, value in kwargs.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        obj.full_clean()
        obj.save()

    def try_to_update(self, obj: Model, **kwargs):
        """Пытается изменить объект obj непосредственно в БД.
        Параметр kwargs - словарь с парами "поле-значение".
        """
        str_kwargs = f"{kwargs}"
        try:
            self.update(obj, **kwargs)
        except Exception as e:
            raise AssertionError(
                f"При обновлении объекта модели "
                f"'{self.get_model().__name__}' с "
                f"корректными данными возникает исключение '{e}'."
                f"Использовались следующие данные: {str_kwargs}"
            )

    def objects_count_test(self, estimated_count: int, err_msg: str):
        """Тестирует на количество объектов."""
        count = self.get_model().objects.count()
        self.assertEqual(count, estimated_count, msg=err_msg)

    def is_exists(self, **obj_kwargs):
        """Проверяет, существует ли объект."""
        return self.get_model().objects.filter(**obj_kwargs).exists()

    def assert_object_exist(self, err_msg: str, **obj_kwargs):
        """Тестирует на существование объекта."""
        for key in (
            "diagnosis",
            "discipline_name",
            "discipline_level",
            "password",
        ):
            if obj_kwargs.get(key, None):
                obj_kwargs.pop(key)
        self.assertTrue(self.is_exists(**obj_kwargs), err_msg)

    def assert_object_not_exist(self, err_msg: str, **obj_kwargs):
        """Тестирует на несуществование объекта."""
        if obj_kwargs.get("password", None):
            obj_kwargs.pop("password")
        self.assertFalse(self.is_exists(**obj_kwargs), err_msg)

    def correct_create_tests(
        self,
        model_correct_schema: dict | None = None,
        url: str | None = None,
        **additional_url_kwargs,
    ):
        """Основной метод тестирования на корректное создание объекта.
        Для тестирования через url - передайте соответствующий параметр и
        (при необходимости) additional_url_kwargs - словарь с дополнительным
        контекстом для POST-запроса. Параметр model_correct_schema
        предусмотрен для случаев, если по каким-то причинам при вызове
        метода необходимо изменить схему "correct_create", использующуюся
        по умолчанию. Если параметр url не передать, будет тестироваться
        изменение путем программного обращения к БД."""
        schema = model_correct_schema or self.get_correct_create_schema()
        initial_objects_count = self.get_model().objects.count()
        via_url = ""
        if url:
            self.try_to_create_via_url(url, **schema, **additional_url_kwargs)
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

    def correct_update_tests(
        self,
        model_upd_schema: dict | None = None,
        url: str | None = None,
        **additional_url_kwargs,
    ):
        """Основной метод тестирования на корректное изменение объекта.
        Для тестирования через url - передайте соответствующий параметр и
        (при необходимости) additional_url_kwargs - словарь с дополнительным
        контекстом для POST-запроса. Параметр model_correct_schema
        предусмотрен для случаев, если по каким-то причинам при вызове
        метода необходимо изменить схему "correct_update", использующуюся
        по умолчанию. Если параметр url не передать, будет тестироваться
        изменение путем программного обращения к БД."""
        cr_schema = self.get_correct_create_schema()
        upd_schema = model_upd_schema or self.get_correct_update_schema()
        obj = self.try_to_create(**cr_schema)
        via_url = ""
        if url:
            self.try_to_update_via_url(
                url, **upd_schema, **additional_url_kwargs
            )
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

    def correct_delete_tests(
        self, url: str | None = None, **additional_url_kwargs
    ):
        """Основной метод тестирования на корректное изменение объекта.
        Для тестирования через url - передайте соответствующий параметр и
        (при необходимости) additional_url_kwargs - словарь с дополнительным
        контекстом для POST-запроса. Параметр model_correct_schema
        предусмотрен для случаев, если по каким-то причинам при вызове
        метода необходимо изменить схему "correct_update", использующуюся
        по умолчанию. Если параметр url не передать, будет тестироваться
        изменение путем программного обращения к БД."""
        cr_schema = self.get_correct_create_schema()
        obj = self.try_to_create(**cr_schema)
        initial_objects_count = self.get_model().objects.count()
        id = obj.id
        via_url = ""
        if url:
            self.try_to_delete_via_url(url, **additional_url_kwargs)
            via_url = f" через POST-запрос по адресу: {url}"
        else:
            self.try_to_delete(id)
        err_msg = (
            f"После удаления объекта модели "
            f"{self.get_model().__name__}{via_url} количество объектов в БД "
            f"не соответствует ожидаемому."
        )
        self.objects_count_test(initial_objects_count - 1, err_msg=err_msg)

    def update_field(self, obj: Model, url: str | None = None, **field_kwargs):
        """Обновляет одно поле (для теста невалидных значений)."""
        if url:
            schema = self.get_correct_update_schema()
            schema.update(field_kwargs)
            self.try_to_update_via_url(url, **schema)
        else:
            self.update(obj, **field_kwargs)

    def _correct_field_test(
        self, obj: Model, url: str | None = None, **kwargs
    ):
        """Обновляет одно поле (для теста валидных значений)"""
        if url:
            self.try_to_update_via_url(url, **kwargs)
        else:
            self.update(obj, **kwargs)

    @staticmethod
    def _unpack_test_values(field, value):
        """Распаковывает внутренние кортежи отдельного тестового значения
        для поля."""
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
        """Распаковывает и формирует списки для каждой пары поле - тестовое
        значение."""
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
    def _alter_tested_value_info(value: Any, force_value: bool = True) -> str:
        """Формирует часть информационного сообщения теста с
        отображением какое конкретно значение тестировалось."""
        if value or force_value:
            return f"Тестировавшееся значение: '{value}'"
        return ""

    def _incorrect_field_msg_compile(
        self, field, msg, value=None, force_value=True
    ):
        """Формирует информационное сообщение теста НЕВАЛИДНОГО поля."""
        tested_value_info = self._alter_tested_value_info(value, force_value)
        return (
            f"Проверьте, что при попытке сохранения в БД модели"
            f" '{self.get_model().__name__}' с полем '{field}', "
            f"содержащим невалидные данные ({msg}), "
            f"вызывается исключение ValidationError. {tested_value_info}"
        ).strip()

    def _incorrect_field_via_url_msg_compile(
        self, field, msg, url, value=None, force_value=True
    ):
        """Формирует информационное сообщение url-теста НЕВАЛИДНОГО поля."""
        tested_value_info = self._alter_tested_value_info(value, force_value)
        return (
            f"Проверьте, что POST-запрос по адресу '{url}'  "
            f"содержащий невалидные данные для поля '{field}' модели"
            f" '{self.get_model().__name__}' ({msg}), "
            f"возвращает ответ со статус-кодом 200(OK) или 302(FOUND) и "
            f"объект в БД не изменяется."
            f" {tested_value_info}"
        ).strip()

    def _correct_field_msg_compile(
        self, field, msg, url, value=None, force_value=True
    ):
        """Формирует информационное сообщение теста ВАЛИДНОГО поля."""
        tested_value_info = self._alter_tested_value_info(value, force_value)
        if url:
            return self._correct_field_via_url_msg_compile(
                field, msg, url, value, force_value
            )
        return (
            f"Проверьте, что в поле '{field}' модели "
            f"'{self.get_model().__name__}' допускается сохранение и не "
            f"вызывает ошибки валидации такие валидные данные, как "
            f"'{msg}'. {tested_value_info}"
        ).strip()

    def _correct_field_via_url_msg_compile(
        self, field, msg, url, value=None, force_value=True
    ):
        """Формирует информационное сообщение url-теста ВАЛИДНОГО поля."""
        tested_value_info = self._alter_tested_value_info(value, force_value)
        return (
            f"Проверьте, что POST-запрос по адресу '{url}'  "
            f"содержащий такие валидные данные для поля '{field}' модели "
            f"'{self.get_model().__name__}', как '{msg}', "
            f"возвращает ответ со статус-кодом 200(OK) или 302(FOUND) и "
            f"изменения сохраняются в БД. {tested_value_info}"
        ).strip()

    def _incorrect_field_sub_test_via_url(
        self, url: str, test: dict, sub: bool = True, **additional_url_kwargs
    ):
        """Проводит отдельный тест поля через url.
        - Словарь test должен содержать ключи "field", "value", "msg".
        - Параметр sub определяет, будет ли тест запускаться с помощью
            subTest. В случае sub == True (по умолчанию) при падении одного
            теста, остальные за пределами данного метода - продолжатся.
            False - остановятся.
        - Параметр additional_url_kwargs - дополнительный контекст для
            POST-запроса."""
        field, value, msg = test["field"], test["value"], test["msg"]
        field_kwargs = {field: value}
        schema = self.get_correct_update_schema()
        schema.update(field_kwargs)
        err_msg = (
            f"Проверьте, что POST-запрос по адресу '{url}',  "
            f"содержащий невалидные данные для поля {field} модели "
            f"'{self.get_model().__name__}' ({msg}), "
            f"возвращает ответ со статус-кодом '200(OK)' или '302(FOUND)'. "
            f"{self._alter_tested_value_info(value, True)}"
        ).strip()
        response = self.try_to_update_via_url(
            url, **schema, **additional_url_kwargs
        )
        self.assertIn(
            response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND], err_msg
        )
        err_msg = (
            f"В результате POST-запроса по адресу '{url}'  "
            f"содержащего невалидные данные для поля '{field}' модели "
            f"'{self.get_model().__name__}' ({msg}), "
            f"объект с указанными невалидными данными обнаруживается в "
            f"БД. {self._alter_tested_value_info(value, True)}"
        ).strip()
        if sub:
            with self.subTest(msg=err_msg):
                self.assert_object_not_exist(msg, **schema)
        else:
            self.assert_object_not_exist(err_msg, **schema)

    def _incorrect_field_sub_test(self, test, obj, sub):
        """Проводит отдельный тест невалидного значения поля через
        попытку записи непосредственно в БД с помощью методов модели Django.
        - Словарь test должен содержать ключи "field", "value", "msg".
        - Параметр sub определяет, будет ли тест запускаться с помощью
            subTest. В случае sub == True (по умолчанию) при падении одного
            теста, остальные за пределами данного метода - продолжатся.
            False - остановятся.
        - Параметр additional_url_kwargs - дополнительный контекст для
            POST-запроса."""
        field = test["field"]
        msg = test["msg"]
        value = test["value"]
        msg = self._incorrect_field_msg_compile(field, msg, value)
        kwargs = {test["field"]: test["value"]}

        def _inner_assert():
            with transaction.atomic():
                self.assertRaises(
                    (ValidationError, ValueError),
                    self.update_field,
                    obj,
                    None,
                    **kwargs,
                )

        if sub:
            with self.subTest(msg=msg):
                _inner_assert()
        else:
            self.update_field(obj=obj, **kwargs)
        # Приводим объект обратно в заведомо валидное состояние.
        self.try_to_update(obj, **self.get_correct_update_schema())

    def _get_field_tests_set(
        self, schemas: Iterable, create_obj: bool = True
    ) -> tuple | tuple[tuple, Model]:
        """Возвращает коллекцию всех тестов всех полей, указанных в схеме.
        - Параметр "schemas" - список всех тестов (т.е. значение ключа
        "must_not_be_admitted" или "must_be_admitted";
        - Параметр "create_obj" - если равен True (по умолчанию), то метод
        также создаст и вернет корректный объект, над которым впоследствии
        можно проводить тесты поля."""
        tests_set = []
        for test_item in schemas:
            tests_set += self._unpack_field_tests(test_item)
        if create_obj:
            obj = self.try_to_create(**self.get_correct_update_schema())
            return tuple(tests_set), obj
        return tuple(tests_set)

    def incorrect_field_tests_via_url(self, url: str, **additional_url_kwargs):
        """Основной метод url-тестирования на некорректное значение поля.
        При необходимости передайте в параметре additional_url_kwargs -
        словарь с дополнительным контекстом для POST-запроса."""
        schemas = self.get_must_not_be_admitted_schemas()
        tests_set, _ = self._get_field_tests_set(schemas, create_obj=True)
        for batch_test in tests_set:
            if isinstance(batch_test, dict):
                self._incorrect_field_sub_test_via_url(
                    url, batch_test, **additional_url_kwargs
                )
            else:
                for test in batch_test:
                    assertion_error = None
                    try:
                        self._incorrect_field_sub_test_via_url(
                            url, test, sub=False, **additional_url_kwargs
                        )
                    except AssertionError as e:
                        err_msg = e.args[0]
                        with self.subTest(msg=err_msg):
                            assertion_error = e
                            raise e
                    finally:
                        if assertion_error:
                            break

    def incorrect_field_tests(self):
        """Основной метод тестирования на некорректное значение поля.
        В отличие от остальных "основных" методов тестирования, не имеет
        собственного параметра url. Для тестирования через url используйте
        отдельный метод incorrect_field_tests_via_url()."""
        schemas = self.get_must_not_be_admitted_schemas()
        tests_set, obj = self._get_field_tests_set(schemas, create_obj=True)
        for batch_test in tests_set:
            if isinstance(batch_test, dict):
                self._incorrect_field_sub_test(
                    test=batch_test, obj=obj, sub=True
                )
            else:
                for test in batch_test:
                    msg = self._incorrect_field_msg_compile(
                        test["field"], test["msg"], test["value"]
                    )
                    exception = None
                    try:
                        self._incorrect_field_sub_test(
                            test=test, obj=obj, sub=False
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
        """Основной метод тестирования ВАЛИДНОГО значения поля.
        Для тестирования через url передайте путь в параметре url/
        В параметре kwargs передайте словарь с дополнительными
        преобразованиями для схемы модели и (или) дополнительным контентом для
        POST-запроса."""
        schema = self.get_must_be_admitted_schema()
        correct_schema = self.get_correct_update_schema()
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
                    self._correct_field_test(obj, url, **update_schema)
                    self.assertTrue(
                        self.get_model().objects.filter(**kwargs).exists(),
                        msg=msg,
                    )
