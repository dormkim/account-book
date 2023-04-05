FROM python:3.9-slim-buster

ENV POETRY_VERSION=1.2.0 \
  PYTHONUNBUFFERED=1

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev

# Creating folders, and files for a project:
COPY . /code
