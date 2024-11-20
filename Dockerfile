FROM python:3.11-alpine

ENV POETRY_HOME='/usr/local' PYTHONUNBUFFERED=1
RUN apk update && apk add curl postgresql-dev &&  curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /report
COPY . /report/

RUN poetry install && mkdir -p "/media"

CMD source /report/start_worker_django.sh