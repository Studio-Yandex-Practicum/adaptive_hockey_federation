# Filename: Dockerfile
# Full path: infra/dev/Dockerfile
# Description: Dockerfile for local development environment

FROM python:3.11-slim

WORKDIR /app
COPY ./poetry.lock ./
COPY ./pyproject.toml ./

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry==1.7.1
RUN poetry config virtualenvs.in-project true
RUN poetry install --with dev

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY adaptive_hockey_federation/ ./
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/app/.venv/bin/gunicorn", "adaptive_hockey_federation.wsgi:application", "--bind", "0:8000" ]
