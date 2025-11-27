from fastapi.testclient import TestClient

from main import app, reset_state


client = TestClient(app)


def setup_function() -> None:
    reset_state()


def test_create_task_returns_created_payload() -> None:
    response = client.post("/tasks", json={"title": "Primera tarea"})
    assert response.status_code == 201
    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Primera tarea"
    assert data["description"] is None


def test_list_tasks_returns_all_created_tasks() -> None:
    client.post("/tasks", json={"title": "Tarea 1"})
    client.post("/tasks", json={"title": "Tarea 2", "description": "Detalle"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Tarea 1"
    assert data[1]["description"] == "Detalle"


def test_delete_task_removes_item() -> None:
    client.post("/tasks", json={"title": "Borrar esto"})
    client.post("/tasks", json={"title": "Mantener esto"})

    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Task deleted"}

    remaining = client.get("/tasks").json()
    assert len(remaining) == 1
    assert remaining[0]["id"] == 2


def test_delete_non_existent_task_returns_404() -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
