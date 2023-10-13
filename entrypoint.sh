#!/bin/sh

sleep 10

source app/.venv/bin/activate

#python manage.py migrate

python manage.py collectstatic  --noinput
mv /static/* /app/static/


exec "$@"