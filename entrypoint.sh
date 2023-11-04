#!/bin/sh

sleep 10
app/.venv/bin/python manage.py collectstatic  --noinput
mv /static/* /app/static/

exec "$@"