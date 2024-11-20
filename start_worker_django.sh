#!/bin/bash

poetry run celery -A api.celery flower --port=5555 &
poetry run python manage.py migrate &&
poetry run celery -A api.celery worker &
poetry run python manage.py runserver 0.0.0.0:8000 --insecure