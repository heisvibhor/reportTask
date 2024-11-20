# Report Task

### RUN

Make sure docker is running on the system.

`docker-compose up --build`

This will start the server, worker, postgres, redis and flower monitoring server.

### Access
API at `http://localhost:8000` 

Flower at `http://localhost:5555`

### Design Choices

- Using file storage to store the reports.
- Using text field in postgres to store the report content.
- Adding task_id to the report model to track the task.
- Using task_id as index to optimize the search.
- Using Django Serializer to validate the input.
- Using python-alpine as base image to reduce the image size.

### API

Endpoints defined in `api/urls.py`

Corresponding views in `api/views.py`

Add task to generate html report

`POST /assignment/html`

Sample Input

```json
{
  "namespace": "ns_example",
  "student_id": "00a9a76518624b02b0ed57263606fc26",
  "events": [
    {
      "type": "saved_code",
      "created_time": "2024-07-21 03:04:55.939000+00:00",
      "unit": "17"
    }
  ]
}
```

Validates the json, enqueues the task and returns task_id

---
Get the status of the task and get the report

Returns task_id

`GET /assignment/html/<task_id>`

```json
{
    "task_id": "00a9a76518624b02b0ed57263606fc26",
    "status": "SUCCESS",
    "data": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2024-07-21T03:04:55.939000Z",
      "task_id": "123e4567-e89b-12d3-a456-426614174001",
      "report": "This is the report content.",
      "report_url": "123e4567-e89b-12d3-a456-426614174002.pdf",
      "student_id": "123e4567-e89b-12d3-a456-426614174002"
    },
    "message": "Task completed"
}
```

Returns the html report, if task is successful and competed. Otherwise, returns the status of the task with data null.

---

`POST /assignment/pdf`

Sample Input

```json
{
  "namespace": "ns_example",
  "student_id": "00a9a76518624b02b0ed57263606fc26",
  "events": [
    {
      "type": "saved_code",
      "created_time": "2024-07-21 03:04:55.939000+00:00",
      "unit": "17"
    }
  ]
}
```

Validates the json, enqueues the task and returns task_id

---

Get the status of the task and get the pdf report as an attachment

`GET /assignment/pdf/<task_id>`

```json
{
    "task_id": "00a9a76518624b02b0ed57263606fc26",
    "status": "PENDING",
    "message": "Task not completed or not found"
}
```

Returns the pdf report, if task is sucessful and competed. Otherwise, returns the status of the task.

## Run Without Docker

### Requirements

- Python 3.11
- Redis
- Postgres-16

### Setup

- Create a virtual environment
- Install poetry `https://python-poetry.org/docs/`
- Run `poetry install`
- Change the database settings in `reportTask/settings.py` to your local postgres settings.
- Change the redis settings in `reportTask/settings.py` to your local redis settings.
- Run 
```
poetry run celery -A api.celery flower --port=5555 &
poetry run python manage.py migrate &&
poetry run celery -A api.celery worker &
poetry run python manage.py runserver 0.0.0.0:8000 --insecure 
```