FROM python:3.11

WORKDIR /app

COPY requirements/production.txt .
RUN pip install -r production.txt --no-cache-dir

COPY . .

WORKDIR /app/adaptive_hockey_federation

# CMD ["gunicorn", "core.wsgi:application", "--bind", "0:8000" ]
