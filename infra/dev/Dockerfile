FROM python:3.11-slim AS builder

RUN mkdir /app
WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry==1.6.1
RUN poetry config virtualenvs.in-project true
RUN poetry install --without dev --with test

FROM python:3.11-slim

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY --from=builder /app /app
COPY adaptive_hockey_federation/ ./
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/app/.venv/bin/gunicorn", "adaptive_hockey_federation.wsgi:application", "--bind", "0:8000" ]
