# tests/test_rest_integration.py
from fastapi.testclient import TestClient
from app.main import app
from app.model import tasks_db

client = TestClient(app)


def setup_function():
    """Limpiar la base de datos antes de cada prueba"""
    tasks_db.clear()


def test_create_and_retrieve_task():
    """Prueba flujo completo de creación y recuperación de tarea"""
    # Crear tarea
    create_response = client.post(
        "/tasks/",
        json={"title": "Integration Test Task", "description": "Test Description"},
    )
    assert create_response.status_code == 200
    created_task = create_response.json()

    # Verificar datos de la tarea creada
    assert created_task["title"] == "Integration Test Task"
    assert created_task["description"] == "Test Description"
    assert created_task["completed"] is False

    # Recuperar tarea
    task_id = created_task["id"]
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    retrieved_task = get_response.json()

    # Comparar tareas
    assert retrieved_task == created_task


def test_update_task_workflow():
    """Prueba flujo completo de actualización de tarea"""
    # Crear tarea inicial
    create_response = client.post(
        "/tasks/", json={"title": "Task to Update", "completed": False}
    )
    created_task = create_response.json()
    task_id = created_task["id"]

    # Actualizar tarea
    update_response = client.put(
        f"/tasks/{task_id}", json={"title": "Updated Task", "completed": True}
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()

    # Verificar cambios
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True
    assert updated_task["id"] == task_id


def test_delete_task_workflow():
    """Prueba flujo completo de eliminación de tarea"""
    # Crear tarea para eliminar
    create_response = client.post("/tasks/", json={"title": "Task to Delete"})
    created_task = create_response.json()
    task_id = created_task["id"]

    # Eliminar tarea
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Intentar recuperar tarea eliminada
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
