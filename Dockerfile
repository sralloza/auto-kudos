FROM python:3.9-alpine

WORKDIR /code

RUN apk add curl gcc musl-dev

ENV GET_POETRY https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py

RUN curl -sSL ${GET_POETRY} | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /code/

COPY strava_api /code/strava_api

RUN poetry install

RUN which kudos

ENTRYPOINT [ "kudos" ]
