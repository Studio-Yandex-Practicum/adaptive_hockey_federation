#!/bin/sh

sleep 5
app/.venv/bin/python manage.py collectstatic  --noinput
mv /static/* /app/static/

exec "$@"