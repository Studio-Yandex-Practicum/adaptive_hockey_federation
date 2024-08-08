FROM python:3.11

RUN apt update && apt install -y libgl1-mesa-glx

WORKDIR /app

COPY requirements/develop.txt .
RUN pip install -r develop.txt --no-cache-dir

COPY . .

WORKDIR /app/adaptive_hockey_federation


CMD ["gunicorn", "core.wsgi:application", "--bind", "0:8000" ]
