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

##### Установить зависимости

```shell
poetry install --with dev --with test
```

## Локальный запуск

```shell
cd adaptive_hockey_federation
python manage.py runserver
```
