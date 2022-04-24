FROM python:3.9-slim
RUN mkdir /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY poetry.lock pyproject.toml ./
COPY ./app /app/app
COPY ./migrations /app/migrations
COPY ./alembic.ini /app/alembic.ini


RUN pip3 install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

