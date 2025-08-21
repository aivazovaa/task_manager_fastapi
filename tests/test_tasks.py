import uuid
from app.routers.tasks import get_db


def test_create_task_default_status(client):
    payload = {"name": "Task A"}
    r = client.post("/tasks", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert uuid.UUID(data["id"])
    assert data["name"] == "Task A"
    assert data["description"] is None
    assert data["status"] == "created"


def test_create_with_status_and_get(client):
    payload = {"name": "Task B", "status": "in_progress", "description": "Desc"}
    r = client.post("/tasks", json=payload)
    assert r.status_code == 201
    created = r.json()
    rid = created["id"]
    r2 = client.get(f"/tasks/{rid}")
    assert r2.status_code == 200
    got = r2.json()
    assert got == created


def test_list_and_filter(client):
    client.post("/tasks", json={"name": "Alpha"})
    client.post("/tasks", json={"name": "Beta", "status": "completed"})
    client.post("/tasks", json={"name": "Alpine", "status": "in_progress"})
    r = client.get("/tasks")
    assert r.status_code == 200
    all_items = r.json()
    assert all_items["total"] == 3
    r2 = client.get("/tasks", params={"status": "in_progress"})
    assert r2.status_code == 200
    assert r2.json()["total"] == 1
    r3 = client.get("/tasks", params={"q": "Al"})
    assert r3.status_code == 200
    assert r3.json()["total"] == 2


def test_update_task(client):
    r = client.post("/tasks", json={"name": "Old", "description": "D"})
    rid = r.json()["id"]
    r2 = client.put(f"/tasks/{rid}", json={"name": "New", "status": "completed"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["name"] == "New"
    assert data["status"] == "completed"
    assert data["description"] == "D"


def test_delete_task(client):
    r = client.post("/tasks", json={"name": "T"})
    rid = r.json()["id"]
    r2 = client.delete(f"/tasks/{rid}")
    assert r2.status_code == 204
    r3 = client.get(f"/tasks/{rid}")
    assert r3.status_code == 404


def test_validation_errors(client):
    r = client.post("/tasks", json={"name": ""})
    assert r.status_code == 422
    r2 = client.put("/tasks/00000000-0000-0000-0000-000000000000", json={"status": "bad"})
    assert r2.status_code == 422


def test_not_found_on_update_and_delete(client):
    r1 = client.put("/tasks/00000000-0000-0000-0000-000000000001", json={"name": "X"})
    assert r1.status_code == 404
    r2 = client.delete("/tasks/00000000-0000-0000-0000-000000000001")
    assert r2.status_code == 404


def test_list_tasks_empty_db(client):
    r = client.get("/tasks")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 0
    assert data["items"] == []

def test_update_task_description(client):
    r = client.post("/tasks", json={"name": "WithDesc"})
    rid = r.json()["id"]
    r2 = client.put(f"/tasks/{rid}", json={"description": "New description"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["description"] == "New description"


def test_get_db_generator():
    gen = get_db()
    db = next(gen)
    assert db is not None
    try:
        next(gen)
    except StopIteration:
        pass
