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
