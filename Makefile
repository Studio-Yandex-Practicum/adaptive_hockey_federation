.PHONY: help
help:
	@echo "Makefile help:"
	@echo "Для автоустановки статики, миграций и регистрации супер юзера, используйте команду "make setup"."
	@echo "Для пошаговой установки используйте ключи: 'collectstatic', 'migrate', 'createsuperuser'."
	@echo "Для запуска веб-приложения используйте ключ 'run'."

setup: collectstatic migrate createsuperuser

collectstatic:
	poetry run python adaptive_hockey_federation/manage.py collectstatic --no-input
migrate:
	poetry run python adaptive_hockey_federation/manage.py migrate --no-input
createsuperuser:
	poetry run python adaptive_hockey_federation/manage.py createsuperuser
run:
	poetry run python adaptive_hockey_federation/manage.py runserver
