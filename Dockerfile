FROM python:3.9-slim-buster

ENV POETRY_VERSION=1.2.0 \
  PYTHONUNBUFFERED=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev

COPY . /code
