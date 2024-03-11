ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

ARG POETRY_VERSION=1.6.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip3 install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /app/

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD gunicorn devices_backend.wsgi:application --bind=0.0.0.0:8000 --reload
