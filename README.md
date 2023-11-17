# Федерация Адаптивного Хоккея

## Описание
Проект для [Федерации адаптивного хоккея](https://paraicehockey.ru/) 
## Технологии
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Poetry](https://python-poetry.org/)
- [Django](https://www.djangoproject.com/)
- [Nginx](https://nginx.org/)
- [Grafana](https://grafana.com/grafana/)

## Подготовка к запуску

##### Клонировать репозиторий

```shell
git clone https://github.com/Studio-Yandex-Practicum/adaptive_hockey_federation.git
```

##### Перейти в директорию

```shell
cd adaptive_hockey_federation
```

##### СОбрать образ и запустить приложение из Dockerfile

```shell
docker build -t adaptive-hockey-federation .
docker run --name adaptive-hockey-federation -it -p 8000:8000 adaptive-hockey-federation
```

## Локальный запуск

```shell
cd adaptive_hockey_federation
python manage.py runserver
```

## Собрать приложения в контейнеры при помощи Docker-compose:

```shell
docker-compose up -d --build
```

Django-проект и Nginx запустятся в контейнерах, при помощи инструкций в entrypoint.sh через 10 секунд добавится статика


## Парсинг файлов

```shell
poetry run parser --path </путь до папки с файлами>
```
Запуск парсера документов для заполнения БД.
Опциональные параметры:
--result Вывод в консоль извлеченных данных и статистики
--help Вызов справки

!!!Необходимо скопировать папку с файлами в контейнер или примонтировать через -volume
