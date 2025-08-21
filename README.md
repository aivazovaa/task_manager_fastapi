
# Менеджер задач (FastAPI)

## Описание
CRUD API для управления задачами. Модель задачи: `uuid`, `name`, `description`, `status` (created | in_progress | completed).

## Стек
- FastAPI
- SQLAlchemy (SQLite)
- pytest
- Docker

## Запуск локально
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
``` 
Swagger UI: http://127.0.0.1:8000/docs  

## Эндпоинты
- `POST /tasks` — создать задачу. Тело: `{ "name": "string", "description": "string|null", "status": "created|in_progress|completed" }`. По умолчанию `status=created`.
- `GET /tasks/{id}` — получить задачу.
- `GET /tasks` — список задач. Параметры: `status`, `q` (поиск по имени), `limit` (1..200), `offset` (>=0).
- `PUT /tasks/{id}` — обновить любую комбинацию полей.
- `DELETE /tasks/{id}` — удалить задачу.

## Тесты
```bash
PYTHONPATH=. pytest -q --cov=app --cov-report=term-missing
```

## Docker
Сборка и запуск:
```bash
docker build -t task-manager .
docker run --rm -p 8000:8000 task-manager
```
или через docker-compose:
```bash
docker compose up --build
```
