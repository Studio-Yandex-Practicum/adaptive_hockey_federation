
# Федерация Адаптивного Хоккея



#### Описание

Проект для [Федерации адаптивного хоккея](https://paraicehockey.ru/)



# Содержание




1. [БРИФ](https://docs.google.com/document/d/1iHkA4Al-H-ppALPJDLMhb_Dl-ciRHH2npM6YRa2HQwg/edit)


1.1. [Инструкции и ритуалы на проекте](docs/materials/instructions.md)



1.2. [ER - диаграмма сущностей](docs/ER_Diagram.jpg)



1.3. [Референс](https://www.youtube.com/watch?v=b0LMWiSynQs)



1.4. [Дизайн](https://www.figma.com/file/8uPoOvMuuJ8hMKASk7hog2/Hokei?type=design&node-id=0-1&mode=design)



2. [О проекте](#project)



2.1. [Структура проекта](#structure)



2.2. [Используемых технологий в проекте](#technologies-project)



3. [Подготовка к запуску](#start)



3.1. [Правила работы с git](#git)



3.2. [Настройка poetry](#poetry)



3.3. [Настройка pre-commit](#pre-commit)



3.4. [Настройка переменных окружения](#env)



4. [Запуск приложения](#run-app)



4.1. [Запуск проекта локально](#run-local)



4.2. [Запуск в Docker](#run-docker)



4.3. [Парсинг файлов](#parsing)



5. [Требования к тестам](#test-app)



6. [Работа с API](#api)



<br><br>



# 2. О проекте <a id="project"></a>



## 2.1 Структура проекта <a id="structure"></a>



| Имя | Описание |

| ------------- | ------------- |

| infrastructure | Docker-compose файлы для запуска проекта с помощью Docker |

| adaptive_hockey_federation | основной код приложения |



## 2.2 Используемые технологии в проекте<a id="technologies-project"></a>:



[![Python][Python-badge]][Python-url]

[![Poetry][Poetry-badge]][Poetry-url]

[![Pre-commit][Pre-commit-badge]][Pre-commit-url]

[![Django][Django-badge]][Django-url]

[![Docker][Docker-badge]][Docker-url]

[![Postgres][Postgres-badge]][Postgres-url]



# 3. Подготовка к запуску <a id="start"></a>



Примечание: для работы над проектом необходим Python не ниже версии 3.11.

Также необходимо установить Poetry (не ниже 1.5.0) и pre-commit.



## 3.1. Правила работы с git (как делать коммиты и pull request-ы)<a id="git"></a>:



1. Две основные ветки: `master` и `dev`

2. Ветка `dev` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код

3. Создавая новую ветку, наследуйтесь от ветки `dev`

4. В `master` находится только production-ready код (CI/CD)

5. Правила именования веток

- весь новый функционал — `feature/название-функционала`

- исправление ошибок — `bugfix/название-багфикса`

6. Пушим свою ветку в репозиторий и открываем Pull Request

7. ВАЖНО! К таске из Projects привязываем свой Pull Request



## 3.2. Poetry (инструмент для работы с виртуальным окружением и сборки пакетов)<a id="poetry"></a>:




Poetry - это инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки пакетов. В этом проекте Poetry необходим для дальнейшей разработки приложения, его установка <b>обязательна</b>.<br>



<details>

<summary>

Как скачать и установить?

</summary>



### Установка:



Установите poetry, не ниже версии 1.5.0 следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).

<details>

<summary>

Команды для установки:

</summary>



Если у Вас уже установлен менеджер пакетов pip, то можно установить командой:



>  *pip install poetry==1.5.0*



Если по каким-то причинам через pip не устанавливается,

то для UNIX-систем и Bash on Windows вводим в консоль следующую команду:



>  *curl -sSL https://install.python-poetry.org | python -*



Для WINDOWS PowerShell:



>  *(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -*



</details>

<br>

После установки перезапустите оболочку и введите команду



> poetry --version



Если установка прошла успешно, вы получите ответ в формате



> Poetry (version 1.5.0)



P.S.: Если при попытке проверить версию возникает ошибка об отсутствии исполняемого файла

(poetry), необходимо после установки добавить его в Path Вашей системы

(пути указаны по ссылке на официальную инструкцию по установке чуть выше.)



Для дальнейшей работы введите команду:



> poetry config virtualenvs.in-project true



Выполнение данной команды необходимо для создания виртуального окружения в

папке проекта.



После предыдущей команды создадим виртуальное окружение нашего проекта с

помощью команды:



> poetry install



Результатом выполнения команды станет создание в корне проекта папки .venv.

Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее)

и pyproject.toml



Для добавления новой зависимости в окружение необходимо выполнить команду



> poetry add <package_name>



_Пример использования:_



> poetry add starlette



Также poetry позволяет разделять зависимости необходимые для разработки, от

основных.

Для добавления зависимости необходимой для разработки и тестирования необходимо

добавить флаг ***--dev***



> poetry add <package_name> --dev



_Пример использования:_



> poetry add pytest --dev



</details>



<details>

<summary>

Порядок работы после настройки

</summary>



<br>



Чтобы активировать виртуальное окружение, введите команду:



> poetry shell



Существует возможность запуска скриптов и команд с помощью команды без

активации окружения:



> poetry run <script_name>.py



_Примеры:_



> poetry run python script_name>.py

>

> poetry run pytest

>

> poetry run black



Порядок работы в оболочке не меняется. Пример команды для Win:



> python src\run_bot.py



Доступен стандартный метод работы с активацией окружения в терминале с помощью команд:



Для WINDOWS:



> source .venv/Scripts/activate



Для UNIX:



> source .venv/bin/activate



</details>



В этом разделе представлены наиболее часто используемые команды.

Подробнее: https://python-poetry.org/docs/cli/



#### Активировать виртуальное окружение

```shell

poetry  shell

```



#### Добавить зависимость

```shell

poetry  add <package_name>

```



#### Обновить зависимости

```shell

poetry  update

```

## 3.3. Pre-commit (инструмент автоматического запуска различных проверок перед выполнением коммита)<a id="pre-commit"></a>:



<details>

<summary>

Настройка pre-commit

</summary>

<br>

1. Убедиться, что pre-comit установлен:



```shell

pre-commit  --version

```

2. Настроить git hook скрипт:



```shell

pre-commit install

```



Далее при каждом коммите у вас будет происходить автоматическая проверка
линтером, а так же будет происходить автоматическое приведение к единому стилю.

</details>



## 3.4. Настройка переменных окружения <a id="env"></a>



Перед запуском проекта необходимо создать копию файла

```.env.example```, назвав его ```.env``` и установить значение токена бота, базы данных почты и тд.



# 4. Запуск приложения <a id="run-app"></a>



##### Клонировать репозиторий



```shell

git  clone  https://github.com/Studio-Yandex-Practicum/adaptive_hockey_federation.git

```



##### Перейти в директорию



```shell

cd  adaptive_hockey_federation

```



## 4.1. Запуск проекта локально <a id="run-local"></a>
Для удобного пользования проектом на локальном компьютере,  реализованы короткие make команды.
1. После клонирования проекта перейдите в корневую директорию проекта при помощи консоли.
```bash
cd  adaptive_hockey_federation
```
2. Запустить локально контейнер postgres (если не запущен)
```bash
make start-db
```
3. Для быстрого развёртывания проекта воспользуйтесь командой:
```bash
make init-app
```
Скрипт сам соберёт статику, применит к базе готовые миграции и инициализирует создание супер-юзера, вам только понадобится ввести его данные.
4. Для запуска локального сервера используйте команду:
```bash
make run
```
5. Если в модели были внесены изменения воспользуйтесь командой:
```bash
make makemigrations
```
Будут созданы свежие миграции и сразу применены к базе данных.

Более подробно со всеми возможностями можно ознакомится при помощи команды help:
```bash
make help
```


## 4.2. Запуск проекта в Docker <a id="run-docker"></a>



Собрать образ и запустить приложение из Dockerfile



```shell

docker  build  -t  adaptive-hockey-federation  .

docker  run  --name  adaptive-hockey-federation  -it  -p  8000:8000  adaptive-hockey-federation

```



Собрать приложения в контейнеры при помощи Docker-compose:



```shell

docker-compose  up  -d  --build

```



Django-проект и Nginx запустятся в контейнерах, при помощи инструкций в entrypoint.sh через 10 секунд добавится статика



## 4.3. Парсинг файлов <a id="parsing"></a>

Файлы документов для парсинга копируем в директорию ``` /<корневая директория>/adaptive_hockey_federation/resourses/```

Файлы документов для парсинга скачивать с [Google Диска] доступ выдается при добавлении в проект
и самый важный файл [Числовые статусы следж-хоккей 02.10.203.docx](https://docs.google.com/document) доступ выдается при добавлении в проект

Запуск парсера документов для заполнения БД производится из корневой директории, короткой командой:
```bash
make fill-db
```

В случае не успешного запуска воспользуйтесь альтернативным способом:
```bash
poetry run parser -r -p  adaptive_hockey_federation/resourses/
```

Результат парсинга сохранится в директории ```/<корневая директория>/adaptive_hockey_federation/core/fixtures/``` в файле

Из ```data.json``` автоматически загрузятся распарсенные данные в таблицы
main_player
main_staffmember
main_staffteammember


Загрузка реальных данных из файлов документов в формате JSON.
**Внимание!** Перед загрузкой файлов из JSON базы и сиквенсы очищаются.
Файлы документов в формате JSON получать у Тимлида проекта в виде архива.

```bash
make fill-db -f
```

В случае не успешного запуска воспользуйтесь альтернативным способом:
```bash
cd ```/<корневая директория>/adaptive_hockey_federation/```
python3 manage.py fill-db -f
```

Опциональные параметры:
-f, --fixtures - Загрузка реальных данных из файлов документов в формате JSON.
**Внимание!** Перед загрузкой файлов из JSON базы и сиквенсы очищаются.
Файлы документов в формате JSON получать у Тимлида проекта в виде архива.


-p, --path - Путь до директории с документами.
-h, --help - Вызов справки.

!!!Необходимо скопировать папку с файлами в контейнер или примонтировать через -volume



# 5. Требования к тестам <a id="test-app"></a>



#### Запуск тестов

Все тесты запускаются командой:

```shell

pytest

```



Или



```shell

make  run_tests

```

Выборочно тесты запускаются с указанием выбранного файла:

```shell

pytest  test_start.py

```



Или



```shell

make  run_unit_tests

```



#### Написание тестов

Для написания тестов используется pytest.

Фикстуры хранятся в файле tests/conftest.py

Основные тесты хранятся в директории tests.

В зависимости от функционала тестов можно добавлять файлы тестов.

Файлы тестов должны начинаться с "test_".



#### Что необходимо тестировать

Разработчик самостоятельно определяет функционал, который будет покрыт

данными. Но, как правило, рекомендуется тестировать все написанные

самостоятельно основные вьюхи, функции отправки и получения сообщений,

функции перенаправления на сторонние или внутренние ресурсы.



#### Рекомендации к написанию кода [Codestyle](docs/codestyle.md)



# 6. Работа с API <a id="api"></a>



#### Доступ к документации API осуществляется по ссылкке (локальный доступ):
```sell
http://127.0.0.1:8000/docs/
```
Для корректного выполнения запросов из Swagger необходимов нажать кнопку ```Authorize```

и ввести API ключ.

При выполнении прямых запросов к эндпоинтам, необходимо добавить в заголовок запроса

ключ ```X-API-KEY``` со значением API ключа.

API ключ вынесен в ```.env.example``` файл. Для удобства работы в локальной среде

установлено значение по умолчанию.




<!-- MARKDOWN LINKS & BADGES -->



[Python-url]: https://www.python.org/downloads/release/python-3110/

[Python-badge]: https://img.shields.io/badge/python-v3.11-yellow?style=for-the-badge&logo=python



[Poetry-url]: https://python-poetry.org/

[Poetry-badge]: https://img.shields.io/badge/poetry-blue?style=for-the-badge&logo=poetry



[Pre-commit-url]: https://pre-commit.com/

[Pre-commit-badge]: https://img.shields.io/badge/Pre--commit-teal?style=for-the-badge&logo=precommit



[Django-url]: https://docs.djangoproject.com/en/4.2/releases/4.2.6/

[Django-badge]: https://img.shields.io/badge/Django-v4.2.6-008000?logo=django&style=for-the-badge



[Docker-url]: https://www.docker.com/

[Docker-badge]: https://img.shields.io/badge/docker-red?style=for-the-badge&logo=docker



[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgresql-gray?style=for-the-badge&logo=postgresql
