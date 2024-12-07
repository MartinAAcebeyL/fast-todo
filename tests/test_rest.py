from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    task_data = {"title": "Test Task", "description": "Test Description"}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task():
    task_data = {"title": "Another Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task():
    task_data = {"title": "Update Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    update_data = {"title": "Updated Title", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["completed"] == True


def test_delete_task():
    task_data = {"title": "Delete Task"}
    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
